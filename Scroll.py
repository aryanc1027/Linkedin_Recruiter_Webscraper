import time


def scrollToBottom(driver):
    start = time.time()

    # will be used in the while loop
    initialScroll = 0
    finalScroll = 1000

    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 1000

        # we will stop the script for 3 seconds so that
        # the data can load
        time.sleep(3)
        # You can change it as per your needs and internet speed

        end = time.time()

        # scroll for 6 seconds
        if round(end - start) > 6:
            break


def scrollLittle(driver):
    start = time.time()

    # will be used in the while loop
    initialScroll = 0
    finalScroll = 500

    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 1000

        # we will stop the script for 3 seconds so that
        # the data can load
        time.sleep(2)
        # You can change it as per your needs and internet speed

        end = time.time()

        # scroll for 4 seconds
        if round(end - start) > 4:
            break