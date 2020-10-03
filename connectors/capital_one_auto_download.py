from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

 # THIS DOES NOT WORK BECAUSE CAPITAL ONE WON"T ALLOW THE LOGIN!!
firefox = '/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox-bin'

def get_browser():
    opts = Options()
    # opts.set_preference('headless', True)
    # opts.set_headless()
    # assert opts.headless  # Operating in headless mode
    return Firefox(options=opts, firefox_binary=firefox)


if __name__ == '__main__':
    browser = get_browser();
    print('got browser')

    browser.get('https://myaccounts.capitalone.com/accountSummary')

    print('got the page')
    browser.implicitly_wait(20)

    print('waiting')

    username = browser.find_element_by_id('ods-input-0')
    password = browser.find_element_by_id('ods-input-1')
    submit = browser.find_element_by_class_name('sign-in-button')

    actions = ActionChains(browser)
    actions.send_keys_to_element(username, 'myusername')
    actions.send_keys_to_element(password, 'mypasword')
    actions.click(on_element=submit)

    actions.perform()

    print(browser.find_element_by_class_name('account-tile__main'))

