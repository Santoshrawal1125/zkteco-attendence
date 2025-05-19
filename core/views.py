# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Define global variable at module level
last_posted_data = None

@csrf_exempt
def iclock_cdata(request):
    global last_posted_data
    if request.method == "POST":
        data = request.body.decode('utf-8')
        last_posted_data = data
        print("📥 Received from device:\n", data)
        return HttpResponse(f"<pre>📥 Received from device:\n\n{data}</pre>")
    else:
        response_text = "Method Not Allowed"
        if last_posted_data:
            response_text += f"\n\nLast received POST data:\n{last_posted_data}"
            response_text = response_text.replace('\n', '<br>')  # for HTML line breaks
        return HttpResponse(response_text, status=405)


def get_request(request):
    return HttpResponse("OK")


