from lib.info_handler import InfoHandler  # Assuming your class is defined in a file named info_handler.py

def run_info_handler_tests():
    info_handler = InfoHandler()

    # session_id_to_check = '7a76d2'
    task_id = '1dc3bdff-8f8c-4fbd-baf6-74de4b7c5958'
    # is_registered = info_handler.is_registered_session(session_id_to_check)
    # print(f"Is session {session_id_to_check} registered? {is_registered}")

    result = info_handler.get_task_result(task_id)

    print(result)

if __name__ == "__main__":
    run_info_handler_tests()
