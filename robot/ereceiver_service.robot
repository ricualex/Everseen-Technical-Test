# Run tests using <robot --loglevel TRACE ./robot/ereceiver_service.robot> command. (Robotframework and Robotframework-requestslibrary must be installed).

*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    BuiltIn

Suite Setup  Create Session    evertest_session    ${BASE_URL}
Suite Teardown  Delete All Sessions

*** Variables ***
${BASE_URL}    http://0.0.0.0:8080/api/v1/data
${HEADERS}     {"Content-Type": "application/json"}


*** Test Cases ***
Successful Scenario With Status Complete
    [Documentation]    Test POST request with "status=complete", "type=1", and valid hash.
    ${payload}=    Create Dictionary    status=complete    type=1    hash=661f8009fa8e56a9d0e94a0a644397d7
    Run API Test    ${payload}    200

Successful Scenario With Status Incomplete
    [Documentation]    Test POST request with "status=incomplete", "type=1", and valid hash.
    ${payload}=    Create Dictionary    status=incomplete    type=1    hash=661f8009fa8e56a9d0e94a0a644397d7
    Run API Test    ${payload}    200

Successful Scenario With Status Cancelled
    [Documentation]    Test POST request with "status=cancelled", "type=1", and valid hash.
    ${payload}=    Create Dictionary    status=cancelled    type=1    hash=661f8009fa8e56a9d0e94a0a644397d7
    Run API Test    ${payload}    200

Unsuccessful Scenario With Status Invalid
    [Documentation]    Test POST request with "status=invalid", "type=1", and valid hash.
    ${payload}=    Create Dictionary    status=invalid    type=1    hash=661f8009fa8e56a9d0e94a0a644397d7
    Run API Test And Expect Error    ${payload}

Successful Scenario With Type Value 1
    [Documentation]    Test POST request with "status=complete", "type=1", and valid hash.
    ${payload}=    Create Dictionary    status=complete    type=1    hash=661f8009fa8e56a9d0e94a0a644397d7
    Run API Test    ${payload}    200

Successful Scenario With Type Value 2
    [Documentation]    Test POST request with "status=complete", "type=2", and valid hash.
    ${payload}=    Create Dictionary    status=complete    type=2    hash=661f8009fa8e56a9d0e94a0a644397d7
    Run API Test    ${payload}    200

Successful Scenario With Type Value 5
    [Documentation]    Test POST request with "status=complete", "type=5", and valid hash.
    ${payload}=    Create Dictionary    status=complete    type=5    hash=661f8009fa8e56a9d0e94a0a644397d7
    Run API Test    ${payload}    200

Successful Scenario With Type Value 11
    [Documentation]    Test POST request with "status=complete", "type=11", and valid hash.
    ${payload}=    Create Dictionary    status=complete    type=11    hash=661f8009fa8e56a9d0e94a0a644397d7
    Run API Test    ${payload}    200

Unsuccessful Scenario With Type Value 0 (Invalid)
    [Documentation]    Test POST request with "status=complete", "type=0", and valid hash.
    ${payload}=    Create Dictionary    status=complete    type=0    hash=661f8009fa8e56a9d0e94a0a644397d7
    Run API Test And Expect Error    ${payload}

Successful Scenario With Valid Hash
    [Documentation]    Test POST request with "status=complete", "type=1", and valid hash.
    ${payload}=    Create Dictionary    status=complete    type=1    hash=661f8009fa8e56a9d0e94a0a644397d7
    Run API Test    ${payload}    200

Unsuccessful Scenario With Invalid Hash
    [Documentation]    Test POST request with "status=complete", "type=1", and invalid hash.
    ${payload}=    Create Dictionary    status=complete    type=1    hash=z661f8009fa
    Run API Test And Expect Error    ${payload}

*** Keywords ***

Run API Test
    [Arguments]    ${payload}    ${expected_status}
    ${headers}=    Evaluate    dict(${HEADERS})
    ${response}=  POST On Session   evertest_session    /    json=${payload}    headers=${headers}
    
    Log    Response status: ${response.status_code}
    Log    Response body: ${response.content}
    
    Should Be Equal As Strings    ${expected_status}    ${response.status_code}
    Log    Test passed with expected status code: ${expected_status}

Run API Test And Expect Error
    [Arguments]    ${payload}
    Create Session    evertest_session    ${BASE_URL}
    ${headers}=    Evaluate    dict(${HEADERS})
    Run Keyword And Expect Error  HTTPError: 500 Server Error: Internal Server Error for url: ${BASE_URL}  POST On Session   evertest_session    /    json=${payload}    headers=${headers}
