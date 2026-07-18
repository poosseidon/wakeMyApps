# Dependencies
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from concurrent.futures import ThreadPoolExecutor
import time, logging, os, threading, numpy as np
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler


# Logger setup
logging.basicConfig(
    level = logging.INFO,
    format = '[%(asctime)s] [%(levelname)s]: %(message)s',
    datefmt = '%A, %Y-%m-%d · %H:%M:%S'
)
logger = logging.getLogger(__name__)


# A utility function for setting up options
def setup_options(headless: bool = True) -> Options:
    
    # Creating an options instance
    options = Options()
    
    # Wether to go or not headless
    if headless:
        options.add_argument('--headless')    
    
    # User agent setup  
    user_agent = (
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        )
    options.add_argument(f'user-agent={user_agent}')
    
    # Performance and UI
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    
    # Anti-detection
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    return options


# A utility function for chatting with xplendidAI daily
t0 = datetime.now()
def ask_xplendid_ai(wait: WebDriverWait, driver: webdriver) -> None:
    # Checks if at least 24h has passed
    global t0
    diff_seconds = (datetime.now() - t0).total_seconds()    
    if diff_seconds >= 86_400:
        t0 = datetime.now()
        try:            
            ## 1st: open the chat
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(3)
            ask_ai_path = (
                '//*[@id="root"]/div[1]/div[1]/div/div/div/section/div[1]/div/'
                'div/div/div[22]/div[2]/div/div/div/div/div/button'
            )
            ask_ai_element = By.XPATH, ask_ai_path
            ask_ai_button = wait.until(EC.element_to_be_clickable(ask_ai_element))
            ask_ai_button.click()
            logger.info('Clicked 🖱️ "Ask AI" 🤖 button!')
        
            ## 2nd: write the message
            message = "Hello!\nWhat's confidence intervals?"
            text_input_path = (
                '//*[@id="root"]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div'
                '/div/div/div/div/div[2]/div/div/div[1]'
            )
            text_input_element = By.XPATH, text_input_path
            text_input = wait.until(EC.presence_of_element_located(text_input_element))
            text_input.send_keys(message)
            logger.info('Wrote text 📝 message to 🤖 xplendidAI!')
        
            ## 3rd: send the message
            send_message_path = (
                '//*[@id="root"]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div'
                '/div/div/div/div/div/div[2]/div/div/div[3]/button'
            )
            send_message_element = By.XPATH, send_message_path
            send_message_button = wait.until(EC.element_to_be_clickable(send_message_element))
            send_message_button.click()
            logger.info(f'Sent "{message}" as a routine message to 🤖xplendidAI 🗪...')
        except Exception as e:
            logger.info(f'An error ({type(e).__name__}) occurred while trying to interact with 🤖xplendidAI')
    else:
        logger.info(f'Only 📅 {round(diff_seconds, 2)}s passed since the last time 🤖xplendidAI was used...')


# Installing and uninstalling packages
def install_packages() -> None:
    global t0
    diff_seconds = (datetime.now() - t0).total_seconds()
    if (diff_seconds < 959) or (diff_seconds >= 86_400):
        logger.info('Installing 📂 and uninstalling 🗑️ packages...')
        # ablisk 
        times_ablisk = np.random.randint(4, 8)
        for _ in range(times_ablisk):
            os.system(
                'pip install -q -U --root-user-action=ignore --disable-pip-version-check ablisk' \
                ' && pip uninstall -q -y --root-user-action=ignore --disable-pip-version-check ablisk'
            )
        # ZeitPy 
        times_zeitpy = np.random.randint(1, 3)
        for _ in range(times_zeitpy):
            os.system(
                'pip install -q -U --root-user-action=ignore --disable-pip-version-check zeitpy' \
                ' && pip uninstall -q -y --root-user-action=ignore --disable-pip-version-check zeitpy'
            )
        logger.info(f'Finished installing "ablisk" and "ZeitPy" {times_ablisk} and {times_zeitpy} times, respectively! ✔️')

# A function for waking apps individually
def wake_single_app(page_items: tuple[str, str]) -> None:   
    page, url = page_items
    # Log message for visiting url page
    logger.info(f'Loading ⌛ {page} page...')
    
    #Setting up the driver options
    options = setup_options()
    
    # Assuring webdriver is installed just once
    if not os.path.exists('chrome_driver_path.txt'):
        exe = ChromeDriverManager().install()
        with open('chrome_driver_path.txt', 'w') as f:
            f.write(exe)
    else:
        with open('chrome_driver_path.txt', 'r') as f:
            exe = f.read().strip()

    # Using the webdriver
    service = Service(exe)
    driver = webdriver.Chrome(options = options, service = service)
    driver.get(url)
    
    # Handling wake-up button from streamlit
    if 'streamlit' in url:        
        try: 
            # Waking up xplendid
            wait = WebDriverWait(driver, timeout = 30, poll_frequency = 10)
            wakeup_element = By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/button'
            wake_up_button = wait.until(EC.element_to_be_clickable(wakeup_element))
            wake_up_button.click()        
        except Exception as e:
            if isinstance(e, TimeoutException):
                logger.info('Maybe 🧪 xplendid is already awaken!')
                # Sending a message to the bot
                ask_xplendid_ai(wait, driver)
                # install_packages() # Removed for now to save time
            elif isinstance(e, StaleElementReferenceException):
                logger.info('⛔ Maybe the reference of the wake up button has changed!')
            else:
                logger.info(f'🚩 An error occured: {type(e).__name__}!')
    else:
        pass        
    time.sleep(3 * 60) 
    logger.info(f'Slept enough for loading {page} page. ➜] Quitting...')
    driver.quit() 


# Function for waking all the apps concurrently
i = 0
def wake_apps() -> None:
    pages_dict = {
        'IMDb Recommender': 'https://imdbrecommender.onrender.com',
        'CarPricesPredictor': 'https://domingosdeeulariadumba-carsellingpricepredictor.hf.space',
        'xplendid': 'https://xplendid.streamlit.app'
    }
    global i    
    try: 
        while True:            
                with ThreadPoolExecutor(max_workers = len(pages_dict)) as executor:
                    executor.map(wake_single_app, pages_dict.items())
                i += 1
                ith = str(i) + 'st' if str(i).endswith('1') and not str(i).endswith('11') else \
                      str(i) + 'nd' if str(i).endswith('2') and not str(i).endswith('12') else \
                      str(i) + 'rd' if str(i).endswith('3') and not str(i).endswith('13') else \
                      str(i) + 'th'
                time_sleep = np.random.randint(5, 9)
                logger.info(
                    'Woke all the apps ☕✔️ · '
                    f'This is the {ith} iteration 🚀🎉 · '
                    f'Sleeping for {time_sleep} minutes 🥱💤'
                           )
                time.sleep(time_sleep * 60)            
    except Exception as e:
        logger.info(f'Error: {type(e).__name__}!!!')
    
        
# Creating an HTTP Request Handler instance for health checks
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:       
        uptime = (datetime.now() - t0).total_seconds()
        content = f'Healthy! :)\n\n\nUptime: {round(uptime, 2)}s | Iteration: {i + 1}'.encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_HEAD(self) -> None:
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        
# Starting the health check server
def start_health_checker() -> None:
    port = int(os.environ.get('PORT', 10000))
    server_address = '0.0.0.0', port
    server = HTTPServer(server_address, HealthCheckHandler)
    server.serve_forever()    


if __name__ == '__main__':
    # Starting health check in the background thread
    health_check_thread = threading.Thread(target = start_health_checker, daemon = True)
    health_check_thread.start()
    
    # Running the main app    
    wake_apps()
