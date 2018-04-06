from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.conf import settings
from .models import Account

import sys

class SeleniumTests(StaticLiveServerTestCase):

    PLATFORMS = {
        'linux' : '/atm/static/web_driver/chromedriver_linux',
        'win32' : '/atm/static/web_driver/chromedriver_windows',
        'darwin' : '/atm/static/web_driver/chromedriver_mac'
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(settings.BASE_DIR + cls.PLATFORMS[sys.platform])
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        Account.objects.create(
            account_id='1029384756', 
            account_name='Test Checking', 
            account_pin='2048',
            customer_name='Test User',
            balance='12300',
            daily_limit='500.00'
        )

    def input_valid_atm_card(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/atm/'))
        self.selenium.find_element_by_id('account_number').send_keys('1029384756')
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'pin1'))
        )

    def input_valid_pin(self):
        self.input_valid_atm_card()
        self.selenium.find_element_by_id('number2').click()
        self.selenium.find_element_by_id('number0').click()
        self.selenium.find_element_by_id('number4').click()
        self.selenium.find_element_by_id('number8').click()
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'transaction_prompt'))
        )

    # Test case 1
    def test_valid_atm_card(self):
        self.input_valid_atm_card()
        self.assertIn('Please enter your PIN:', self.selenium.page_source)
    
    # Test case 2
    def test_invalid_atm_card(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/atm/'))
        self.selenium.find_element_by_id('account_number').send_keys('1111111111')
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.alert_is_present()
        )
        alert = self.selenium.switch_to.alert
        self.assertIn('Invalid ATM card. It will be retained.', alert.text)
        alert.accept()

    # Test case 3
    def test_valid_pin(self):
        self.input_valid_pin()
        self.assertIn('Selection transaction:', self.selenium.page_source)
        self.assertIn('Balance', self.selenium.page_source)
        self.assertIn('Deposit', self.selenium.page_source)
        self.assertIn('Withdrawal', self.selenium.page_source)

    # Test case 4
    def test_invalid_pin(self):
        self.input_valid_atm_card()
        self.selenium.find_element_by_id('number1').click()
        self.selenium.find_element_by_id('number2').click()
        self.selenium.find_element_by_id('number3').click()
        self.selenium.find_element_by_id('number4').click()
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.alert_is_present()
        )
        alert = self.selenium.switch_to.alert
        self.assertIn('Invalid PIN. Try agin.', alert.text)
        alert.accept()
        self.selenium.find_element_by_id('number5').click()
        self.selenium.find_element_by_id('number6').click()
        self.selenium.find_element_by_id('number7').click()
        self.selenium.find_element_by_id('number8').click()
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.alert_is_present()
        )
        alert = self.selenium.switch_to.alert
        self.assertIn('Invalid PIN. Try agin.', alert.text)
        alert.accept()
        self.selenium.find_element_by_id('number9').click()
        self.selenium.find_element_by_id('number0').click()
        self.selenium.find_element_by_id('number1').click()
        self.selenium.find_element_by_id('number2').click()
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'welcome_prompt'))
        )
        self.assertIn('Rock Solid Federal Credit Union', self.selenium.page_source)

    # Test case 5
    def test_balance_is_shown(self):
        self.input_valid_pin()
        self.selenium.find_element_by_id('right2').click()
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'total_balance'))
        )
        self.assertIn('Your balance is:', self.selenium.page_source)
        self.assertEqual(
            self.selenium.find_element_by_id('total_balance').get_attribute('innerText'),
            str(Account.objects.get(account_id='1029384756').balance)
        )

    # Test case 6
    def test_valid_deposit(self):
        self.input_valid_pin()
        self.selenium.find_element_by_id('right3').click()
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'amount'))
        )
        self.assertIn('Enter amount to deposit.', self.selenium.page_source)
        self.selenium.find_element_by_id('number4').click()
        self.selenium.find_element_by_id('number5').click()
        self.selenium.find_element_by_id('number0').click()
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.alert_is_present()
        )
        alert = self.selenium.switch_to.alert
        self.assertIn('Please insert deposit into deposit slot.', alert.text)
        alert.accept()
        self.selenium.find_element_by_id('deposit').send_keys('450')
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.alert_is_present()
        )
        alert = self.selenium.switch_to.alert
        self.assertIn('Your new balance is being printed.', alert.text)
        alert.accept()    
        self.assertEqual(self.selenium.find_element_by_id('receipt').get_property('value'), '$12,750.00')

    # Test case 7
    def test_jammed_deposit(self):
        self.input_valid_pin()
        self.selenium.find_element_by_id('right3').click()
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'amount'))
        )
        self.selenium.find_element_by_id('deposit').send_keys('12039')
        self.selenium.find_element_by_id('number4').click()
        self.selenium.find_element_by_id('number5').click()
        self.selenium.find_element_by_id('number0').click()
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.alert_is_present()
        )
        alert = self.selenium.switch_to.alert
        self.assertIn('Temporarily unable to process deposits.', alert.text)
        alert.accept()

    # Test case 8
    def test_valid_withdrawal(self):
        self.input_valid_pin()
        self.selenium.find_element_by_id('right4').click()
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'amount'))
        )
        self.assertIn('Enter amount to withdrawal.', self.selenium.page_source)
        self.selenium.find_element_by_id('number4').click()
        self.selenium.find_element_by_id('number5').click()
        self.selenium.find_element_by_id('number0').click()
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.alert_is_present()
        )
        alert = self.selenium.switch_to.alert
        self.assertIn('Your balance is being updated. Please take cash from dispenser.', alert.text)
        alert.accept()
        self.assertEqual(
            self.selenium.find_element_by_id('receipt').get_property('value'),
            '$11,850.00'
        )
        self.assertEqual(
            self.selenium.find_element_by_id('dispenser').get_property('value'),
            '$450.00'
        )

    # Test case 9
    def test_not_multiple_of_ten_withdrawal(self):
        self.input_valid_pin()
        self.selenium.find_element_by_id('right4').click()
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'amount'))
        )
        self.assertIn('Enter amount to withdrawal.', self.selenium.page_source)
        self.selenium.find_element_by_id('number4').click()
        self.selenium.find_element_by_id('number5').click()
        self.selenium.find_element_by_id('number3').click()
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.alert_is_present()
        )
        alert = self.selenium.switch_to.alert
        self.assertIn('Machine can only dispense $10 notes. Please enter a valid amount.', alert.text)
        alert.accept()

    # Test case 10
    def test_insufficient_funds_withdrawal(self):
        self.input_valid_pin()
        self.selenium.find_element_by_id('right4').click()
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'amount'))
        )
        self.assertIn('Enter amount to withdrawal.', self.selenium.page_source)
        self.selenium.find_element_by_id('number1').click()
        self.selenium.find_element_by_id('number3').click()
        self.selenium.find_element_by_id('number4').click()
        self.selenium.find_element_by_id('number0').click()
        self.selenium.find_element_by_id('number0').click()
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.alert_is_present()
        )
        alert = self.selenium.switch_to.alert
        self.assertIn('Insufficient funds! Please enter a valid amount.', alert.text)
        alert.accept()

    # Test case 11
    def test_daily_limit_exceeded_withdrawal(self):
        self.input_valid_pin()
        self.selenium.find_element_by_id('right4').click()
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, 'amount'))
        )
        self.selenium.find_element_by_id('number5').click()
        self.selenium.find_element_by_id('number3').click()
        self.selenium.find_element_by_id('number0').click()
        self.selenium.find_element_by_id('enter').click()
        WebDriverWait(self.selenium, 5).until(
            EC.alert_is_present()
        )
        alert = self.selenium.switch_to.alert
        self.assertIn('Daily limit exceeded.', alert.text)
        alert.accept()