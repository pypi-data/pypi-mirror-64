def get(driver, params):
    """Get a unique element with Selenium and attributes filters.

    Parameters:
    - driver [selenium] : Selenium driver
    - params [dict] : A dict that contains elements to search the element for
    Returns:
    - element [WebElement] : A single WebElement found
    """
    elements = gets(driver=driver, params=params)
    if len(elements) > 1:
        raise Warning('#pytholenium-Error002#. Searching with: ' + str(params) + '. Found more than 1 element. %s elements were found' % str(len(elements)))
    elif len(elements) == 0:
        raise Warning('#pytholenium-Error003#. Searching with: ' + str(params) + '. No elements were found')
    return elements[0]



def gets(driver, params):
    """Get a list of elements with Selenium and attributes filters.

    Parameters:
    - driver [selenium] : Selenium driver
    - params [dict] : A dict that contains elements to search the element for
    Returns:
    - elements [list of WebElements] : A list of WebElements found
    """
    by_element, by_attribute = __filter_params(params)
    if len(by_element) > 1:
        raise ValueError('#pytholenium-Error001#. No more than 1 item to be searched by element (selenium search) allowed')
    if len(by_element) == 1:
        elements = __get_elements(driver=driver, params=by_element)
    elif len(by_element) == 0:
        elements = __get_elements(driver=driver, params={"css_selector": "*"})
    if len(by_attribute) > 0:
        elements = __get_attributes(elements=elements, params=by_attribute)
    return elements



def wait(driver, params, timeout=10):
    """Set an implicitly wait, by default 10secs, and wait for the element.

    Parameters:
    - driver [selenium] : Selenium driver
    - params [dict] : A dict that contains elements to search the element for
    - timeout [int] : Maximun time to wait for the element
    Returns:
    - element [WebElement] : A single WebElement found
    """
    driver.implicitly_wait(timeout)
    return get(driver=driver, params=params)



def do(driver, params, action, value=None):
    """Makes an action on an element.

    Parameters:
    - driver [selenium] : Selenium driver
    - params [dict] : A dict that contains elements to search the element for
    - action [string] : Action to perform
    - value [string] : Value to input on fields
    Returns:
    - output [string] : In case there is an ouput on the action
    """
    element = get(driver, params)
    perform_dict = {"element": element, "value": value}
    available_actions={
        "click": __click,
        "send_keys": __send_keys,
        "send_enter": __send_enter,
        "send_tab": __send_tab,
        "check": __check,
        "un_check": __un_check,
        "submit": __submit
    }
    perform = available_actions.get(action, None)
    if perform is None:
        raise Warning('#pytholenium-Error004#. Action "' + action + '" is not an available action')
    status, output = perform(perform_dict)
    if not status:
        raise Warning('#pytholenium-Error005#. When performing action: "' + action + '" - ' + output)
    elif output is not None:
        return output



def wait_do(driver, params, action, value=None, timeout=10):
    """Perform wait and do actions.

    Parameters:
    - driver [selenium] : Selenium driver
    - params [dict] : A dict that contains elements to search the element for
    - action [string] : Action to perform
    - value [string] : Value to input on fields
    - timeout [int] : Maximun time to wait for the element
    Returns:
    - output [string] : In case there is an ouput on the action
    """
    wait(driver=driver, params=params, timeout=timeout)
    return do(driver=driver, params=params, action=action, value=value)



def __filter_params(params):
    """Filter the params and return the way to find the object (by_element or by_attribute).

    Parameters:
    - params [dict] : A dict that contains elements to search the element for
    Returns: 
    - by_element [dict] : A dict that contains Selenium filters
    - by_attribute [dict] : A dict that contains attributes filters
    """
    params = params.copy()
    by_element_list = ["id", "name", "xpath", "link_text", "partial_link_text", "tag_name", "class_name", "css_selector"]
    by_element = {}
    by_attribute = {}
    while len(params) > 0:
        key = next(iter(params))
        if key in by_element_list:
            by_element[key] = params.get(key)
        else:
            by_attribute[key] = params.get(key)
        del params[key]
    return by_element, by_attribute



def __get_elements(driver, params):
    """Get elements using Selenium.

    Parameters:
    - driver [selenium] : Selenium driver
    - params [dict] : A dict that contains elements to search the element for
    Returns:
    - output [WebElement list] : A list of found WebElements
    """
    if params.get("id"):
        return [driver.find_element_by_id(params.get("id"))]
    if params.get("name"):
        return driver.find_elements_by_name(params.get("name"))
    elif params.get("xpath"):
        return driver.find_elements_by_xpath(params.get("xpath"))
    elif params.get("link_text"):
        return driver.find_elements_by_link_text(params.get("link_text"))
    elif params.get("partial_link_text"):
        return driver.find_elements_by_partial_link_text(params.get("partial_link_text"))
    elif params.get("tag_name"):
        return driver.find_elements_by_tag_name(params.get("tag_name"))
    elif params.get("class_name"):
        return driver.find_elements_by_class_name(params.get("class_name"))
    elif params.get("css_selector"):
        return driver.find_elements_by_css_selector(params.get("css_selector"))



def __get_attributes(elements, params):
    """Get elements using element's attributes.

    Parameters:
    - elements [list] : List of elements to filter for its attributes
    - params [dict] : A dict that contains elements to search the element for
    Returns:
    - output [WebElement list] : A subset list of found WebElements inside elements argument
    """
    params_tmp = params.copy()
    elements_tmp = elements.copy()
    found = False
    ret_items = []
    while len(params_tmp) > 0:
        for item in elements_tmp:
            key = next(iter(params_tmp))
            #Compare text value attribute
            if key == "text":
                if item.text == params_tmp.get("text"):
                    found = True
            #Compare tag name attribute
            elif key == "tag_name_attribute":
                if item.tag_name == params_tmp.get("tag_name_attribute"):
                    found = True
            #Compare generic attributes
            else:
                if item.get_attribute(key) == params_tmp.get(key):
                    found = True
            if found:
                ret_items.append(item)
            found = False
        #Delete the used attribute filter
        del params_tmp[key]
        #If some attribute matched, now we iterate inside ret_items for upcoming attributes filters
        if len(ret_items) > 0 and len(params_tmp) > 0:
            elements_tmp = ret_items
            ret_items = []
    return ret_items



def __click(perform_dict):
    """Click on element."""
    perform_dict.get("element").click()
    return True, None

def __send_keys(perform_dict):
    """Type on element."""
    perform_dict.get("element").clear()
    perform_dict.get("element").send_keys(perform_dict.get("value"))
    return True, None

def __send_enter(perform_dict):
    """Send enter key."""
    perform_dict.get("element").send_keys(Keys.RETURN)
    return True, None

def __send_tab(perform_dict):
    """Send tab key."""
    perform_dict.get("element").send_keys(Keys.TAB)
    return True, None

def __check(perform_dict):
    """Check checkbox."""
    if not perform_dict.get("element").is_selected():
        perform_dict.get("element").click()
        return True, None
    return False, "Element specified is already checked"

def __un_check(perform_dict):
    """Uncheck checkbox."""
    if perform_dict.get("element").is_selected():
        perform_dict.get("element").click()
        return True, None
    return False, "Element specified is already unchecked"

def __submit(perform_dict):
    """Perform submit."""
    perform_dict.get("element").submit()
    return True, None

def __get_html(perform_dict):
    """Get innerHTML from element."""
    return True, perform_dict.get("element").get_attribute("innerHTML")