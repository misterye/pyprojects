from clockwork import clockwork

api = clockwork.API('428ffed46c979990ec456a6687fe671f6b601fa1')

message = clockwork.SMS(
    to = '8613916838729',
    message = 'This is a test message.')

response = api.send(message)

if response.success:
    print (response.id)
else:
    print (response.error_code)
    print (response.error_message)