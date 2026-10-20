
# S06 - Salesforce Account Automation

def test_account_update():

    # Assumptions:
    # Salesforce API authentication is configured.
    # Test user has Account read and edit permissions.
    # API user can create, read and delete Accounts.
    # Description is an editable Account field.

    account_id = None
    test_id = generate_unique_id()
    updated_value = "Updated by QA " + test_id

    try:
        # Step 1: Create test data using Salesforce API
        account = sf_api.create("Account", {
            "Name": "QA Test Account " + test_id,
            "Description": "Initial test value"
        })

        assert account["success"]
        account_id = account["id"]

        # Step 2: Open the Account in Salesforce Lightning
        browser.login_as("qa_user")

        browser.navigate(
            base_url + "/lightning/r/Account/"
            + account_id + "/view"
        )

        browser.wait_for_visible("Account Details")

        # Step 3: Edit the Account Description
        browser.click("Edit")
        browser.wait_for_visible("Description")

        browser.fill(
            "Description",
            updated_value
        )

        browser.click("Save")

        # Step 4: Wait for UI to reflect the update
        browser.wait_until(
            lambda: browser.get_field_value("Description")
            == updated_value,
            timeout=15000
        )

        # Step 5: Verify saved data through Salesforce API
        def api_value_matches():
            result = sf_api.get(
                "Account",
                account_id
            )
            return result["Description"] == updated_value

        wait_until(
            api_value_matches,
            timeout=15000,
            interval=1000
        )

        print("PASS: Account updated successfully")
        print("Account ID:", account_id)

    except Exception as error:

        # Capture evidence if the test fails
        browser.take_screenshot("failure.png")
        browser.save_logs("test_logs.txt")

        print("FAIL: Account update test failed")
        print("Error:", str(error))
        print("Account ID:", account_id)

        raise

    finally:
        # Step 6: Clean up test data
        if account_id:
            try:
                sf_api.delete("Account", account_id)
                print("Test Account deleted")

            except Exception as cleanup_error:
                print("Cleanup failed:", cleanup_error)
                raise
