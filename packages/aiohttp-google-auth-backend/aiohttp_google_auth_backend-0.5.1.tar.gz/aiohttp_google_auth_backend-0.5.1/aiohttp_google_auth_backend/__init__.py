"""
aiohttp_google_auth_backend: Asyncio
    Copyright (C) 2020  Ketan B Shah, JyotiStar Inc, shahketanb

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import asyncio
import datetime
import logging
import typing

import aiohttp
from dateutil.parser import parse as parse_ts
from google.auth import jwt
from google.oauth2 import id_token

logger = logging.getLogger()


class JSAioGoogleTokenVerifier:

    IDTOKEN_FIELDS = {'email', 'email_verified', 'name', 'picture', 'given_name', 'family_name', 'locale'}

    def __init__(self,
                 profile_fields: typing.Set[str] = None,
                 ok_renew_interval: int = None,
                 min_error_renew_interval: int = 1,
                 max_error_renew_interval: int = 64,
                 timeout: int = 5):
        """

        :param profile_fields: profile fields to be returned
        :param ok_renew_interval: interval in seconds to renew google certificates
        :param min_error_renew_interval: minimum interval to retry,
                when there is issue in getting google certificate
        :param max_error_renew_interval: maximum interval to retry,
                when there is issue in getting google certificate
        :param timeout: Timeout to be used when reading google certificate
        """

        if profile_fields:
            self.profile_fields = set(profile_fields).intersection(self.IDTOKEN_FIELDS)
            if not self.profile_fields:
                raise ValueError('No valid profile field(s) selected')
        else:
            self.profile_fields = {'email'}
        self.certs_lock = asyncio.Lock()
        self.certs = None
        self.ok_renew_interval = ok_renew_interval
        self.min_error_renew_interval = min_error_renew_interval or 1
        self.max_error_renew_interval = max_error_renew_interval or 128
        if self.max_error_renew_interval < self.min_error_renew_interval:
            self.max_error_renew_interval = self.min_error_renew_interval
        self.cur_interval = None
        self.timeout = timeout
        self.cur_task = None

    def _cur_renew_interval(self):
        """ Use exponential backoff to calculate renew interval for next try

        :return: interval to wait for renewal of certificate
        """
        if self.cur_interval is None:
            self.cur_interval = self.min_error_renew_interval
        else:
            self.cur_interval += self.cur_interval
            if self.cur_interval > self.max_error_renew_interval:
                self.cur_interval = self.max_error_renew_interval
        return self.cur_interval

    async def _renew_certs(self):
        """ Uses aiohttp ClientSession to fetch Google OAuth2 certificates

        :return: delay in seconds, before requesting fetch again
        """
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(self.timeout)) as session:
                async with session.get(id_token._GOOGLE_OAUTH2_CERTS_URL) as resp:
                    certs = await resp.json()
                    if not certs or not isinstance(certs, dict):
                        delay = self._cur_renew_interval()
                        logger.warning(f'jsAioGoogleTokenVerifier::_renew_certs no certificates: will retry after {delay} seconds')
                    else:
                        if 'Expires' in resp.headers:
                            expiry_time = parse_ts(resp.headers['Expires'])
                            if expiry_time:
                                delay = (expiry_time - datetime.datetime.now(expiry_time.tzinfo)).seconds
                                # if certificates expiry is longer than renewal interval, use renewal interval
                                if self.ok_renew_interval and delay > self.ok_renew_interval:
                                    delay = self.ok_renew_interval
                        else:
                            delay = self.ok_renew_interval or self.max_error_renew_interval or 3600

                        async with self.certs_lock:
                            self.certs = certs
                            logger.info(f'jsAioGoogleTokenVerifier::_renew_certs renewed certificates: will retry after {delay} seconds')
        except aiohttp.ClientError as err:
            delay = self._cur_renew_interval()
            logger.warning(f'jsAioGoogleTokenVerifier::_renew_certs failed to renew  {err}: will retry after {delay} seconds')
        return delay

    async def _renew_certs_task(self, delay: int):
        """ Asyncio Task to periodically renew Google OAuth2 certificates

        :param delay: Initial delay
        :return:
        """
        logger.debug('jsAioGoogleTokenVerifier::_renew_certs_task background task started')
        try:
            while True:
                await asyncio.sleep(delay)
                delay = await self._renew_certs()
        except asyncio.CancelledError:
            logger.debug('jsAioGoogleTokenVerifier::_renew_certs_task background task shutdown')

    async def on_startup(self):
        """ Hook to start background task to periodically renews google certificates

        :return: None
        """
        delay = await self._renew_certs()
        self.cur_task = asyncio.create_task(self._renew_certs_task(delay))

    async def on_cleanup(self):
        """ Hook to stop background task that periodically renews google certificates

        :return:None
        """
        if self.cur_task:
            self.cur_task.cancel()
            await self.cur_task

    async def verify_token(self, idtoken: str, audience: str):
        """ Verify google token for given audience

        :param idtoken: google token
        :param audience: audience
        :return: dictionary with status field. If success, contains email, otherwise error
        """
        if not idtoken:
            return 401, dict(error=ValueError('token missing'))

        try:
            async with self.certs_lock:
                if not self.certs:
                    return 503, dict(error=ValueError('Service Unavailable'))

                res = jwt.decode(idtoken, certs=self.certs, audience=audience)
                token_fields = {key:value for key, value in res.items() if key in self.profile_fields}
                if token_fields:
                    return 200, token_fields
                else:
                    return 401, dict(error=ValueError("fields missing in token "))
        except ValueError as err:
            return 401, dict(error=err)
