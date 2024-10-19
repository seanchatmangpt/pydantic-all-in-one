# import asyncio
#
# import pytest
#
# from pyd4all.streamer import broker, app, User
# from pyd4all.config import settings
#
# @pytest.mark.asyncio
# async def test_main():
#     # Start the broker and the FastStream application
#     await broker.start()
#     print("[Test] Broker started.")
#
#     # Create a test user message
#     test_user = {"user_id": 1, "user": "Alice"}
#
#     # Publish the test message to the input channel
#     await broker.publish(test_user, settings.input_channel)
#     print(f"[Test] Published message to input channel: {test_user}")
#
#     # Consume the processed message from the output channel
#     processed_message = await broker.consume(settings.output_channel)
#     print(f"[Test] Processed message from output channel: {processed_message}")
#
#     # Validate that the processed message is as expected
#     expected_message = {"message": "User: 1 - Alice registered."}
#     assert processed_message == expected_message, f"Expected {expected_message}, but got {processed_message}"
#
#     print("[Test] Test passed! The processed message matches the expected output.")
#
#     # Close the broker after the test is done
#     await broker.close()
#     print("[Test] Broker stopped.")
#
