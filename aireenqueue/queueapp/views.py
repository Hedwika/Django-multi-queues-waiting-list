from django.shortcuts import render
from django.views.generic import ListView
from queueapp.forms import Newcomer
from django.contrib import messages
from datetime import datetime

class IndexView(ListView):
    template_name = "index.html"

    queue1 = [1, 2, 3]
    queue2 = [4, 5, 6, 7]
    queue3 = [8, 9]

    form = Newcomer()

    progress = {1: ["This number was in queue number 1."],
                2: ["This number was in queue number 1."],
                3: ["This number was in queue number 1."],
                4: ["This number was in queue number 2."],
                5: ["This number was in queue number 2."],
                6: ["This number was in queue number 2."],
                7: ["This number was in queue number 2."],
                8: ["This number was in queue number 3."],
                9: ["This number was in queue number 3."]}

    def log(self, time, type, number, mark):
        return object()

    def get(self, request, *args, **kwargs):
        queue1 = self.queue1
        queue2 = self.queue2
        queue3 = self.queue3

        if '1to2' in request.GET:
            if not queue1:
                note = "There are no numbers in the queue now. Please add one first to be able to remove it."
                messages.error(request, note)
                time = datetime.now()
                type = "error"
                number = "None"
                mark = "empty q1"
                self.log(time, type, number, mark)

            else:
                last = self.queue1[-1]
                self.queue2.append(last)
                self.queue1.pop()
                time = datetime.now()
                type = "success"
                number = last
                mark = "1to2"
                self.log(time, type, number, mark)

                for key in self.progress:
                    if key == last:
                        self.progress[key].append("Was moved to queue number 2.")

        if '2to3' in request.GET:
            if not queue2:
                note = "There are no numbers in the queue now. Please add one first to be able to remove it."
                messages.error(request, note)
                time = datetime.now()
                type = "error"
                number = "None"
                mark = "empty q2"
                self.log(time, type, number, mark)

            else:
                last = self.queue2[-1]
                self.queue3.append(last)
                self.queue2.pop()
                time = datetime.now()
                type = "success"
                number = last
                mark = "2to3"
                self.log(time, type, number, mark)

                for key in self.progress:
                    if key == last:
                        self.progress[key].append("Was moved to queue number 3.")

        if 'remove' in request.GET:
            if not queue3:
                note = "There are no numbers in the queue now. Please add one first to be able to remove it."
                messages.error(request, note)
                time = datetime.now()
                type = "error"
                number = "None"
                mark = "empty q3"
                self.log(time, type, number, mark)

            else:
                last = self.queue3[-1]
                self.queue3.pop()
                time = datetime.now()
                type = "success"
                number = last
                mark = "remove"
                self.log(time, type, number, mark)

                for key in self.progress:
                    if key == last:
                        self.progress[key].append("Was deleted from queue number 3.")

                        message = self.progress[key]
                        listToStr = ' '.join([str(elem) for elem in message])
                        string = "Progress data for user number " + str(last) + ": " + listToStr

                        messages.success(request, string)

                del self.progress[last]

        args = {'queue1': queue1, 'queue2': queue2, 'queue3': queue3, 'form': self.form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = Newcomer(request.POST)

        if form.is_valid():
            number = form.cleaned_data['number']

            if 'add' in request.POST:
                error = False
                for key in self.progress:
                    if number == key:
                        note = "The request with this number is already being processed, please select another number."
                        messages.error(request, note)
                        error = True
                        pass

                if not error:
                    self.queue1.append(number)
                    self.progress[number] = ["The number was added to queue number 1."]

        args = {'queue1': self.queue1, 'queue2': self.queue2, 'queue3': self.queue3, 'form': form}
        return render(request, self.template_name, args)