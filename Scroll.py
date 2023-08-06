import time


def scrollToBottom(driver):
    start = time.time()

    initialScroll = 0
    finalScroll = 1000

    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # Command scrolls from initial pixel 
        # value to final pixel value
        initialScroll = finalScroll
        finalScroll += 1000

        # Allowing data to load completely
        time.sleep(3)

        end = time.time()

        # Scrolls for 6 seconds
        if round(end - start) > 6:
            break


def scrollLittle(driver):
    start = time.time()

    initialScroll = 0
    finalScroll = 500

    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # Command scrolls from initial pixel 
        # value to final pixel value
        initialScroll = finalScroll
        finalScroll += 1000

        # Allowing data to load completely
        time.sleep(2)

        end = time.time()

        # Scrolls for 4 seconds
        if round(end - start) > 4:
            break