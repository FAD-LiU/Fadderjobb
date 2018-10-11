from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from fadderanmalan.models import Job, EnterQueue, LeaveQueue


# TODO Email notifications for dequeueing.
# TODO Support for admin-interaction in queue system.
# TODO View queues in frontend
# If an admin wishes to move a fadder they have to manage the queues manually.


@login_required(login_url="accounts:login")
def register_for_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == "POST":
        if job.full():
            try:  # First try removing ourselves from the lq if we changed our mind
                lq = LeaveQueue.objects.get(job=job, fadder=request.user.fadder)
                lq.delete()

                messages.add_message(request, messages.INFO,
                                     "Din köplats är nu borttagen.")
            except LeaveQueue.DoesNotExist:  # We weren't queued to leave, try to register us
                try:  # If someone else wants to leave, take their slot
                    lq = LeaveQueue.get_first(job=job)
                    job.fadders.remove(lq.fadder)
                    job.fadders.add(request.user.fadder)
                    lq.delete()

                    messages.add_message(request, messages.INFO,
                                         "Du är nu registrerad på passet. Du tog %s:s plats." % lq.fadder.user.username)
                except LeaveQueue.DoesNotExist:  # No one wanted to leave, queue us for enter
                    eq = EnterQueue(job=job, fadder=request.user.fadder)
                    eq.save()

                    messages.add_message(request, messages.INFO,
                                         "Du står nu i kö för passet. Om en fadder lämnar passet kommer du att få det.")
        else:  # Not full, register as normal
            job.fadders.add(request.user.fadder)

            messages.add_message(request, messages.INFO,
                                 "Du är nu registrerad för passet.")

    return redirect("fadderanmalan:jobsignup_detail", job.slug)


@login_required(login_url="accounts:login")
def deregister_for_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == "POST":
        if job.locked:
            try:  # First try removing ourselves from the eq if we changed our mind
                eq = EnterQueue.objects.get(job=job, fadder=request.user.fadder)
                eq.delete()

                messages.add_message(request, messages.INFO,
                                     "Din köplats är nu borttagen.")
            except EnterQueue.DoesNotExist:  # We weren't queued to enter, try to remove us
                try:  # If someone else wants to enter, give the slot to them
                    eq = EnterQueue.get_first(job=job)
                    job.fadders.remove(request.user.fadder)
                    job.fadders.add(eq.fadder)
                    eq.delete()

                    messages.add_message(request, messages.INFO,
                                         "Du är nu avregistrerad från passet. %s tog din plats."
                                         % eq.fadder.user.username)
                except EnterQueue.DoesNotExist:  # No one wanted to enter, queue us for leave
                    lq = LeaveQueue(job=job, fadder=request.user.fadder)
                    lq.save()

                    messages.add_message(request, messages.INFO,
                                         "Du är nu i kön för att avregistrera dig från passet.")
        else:
            job.fadders.remove(request.user.fadder)

            message = "Du är nu avregistrerad från passet."

            try:  # If there is someone queued, give the slot to them
                eq = EnterQueue.get_first(job=job)
                job.fadders.add(eq.fadder)
                eq.delete()

                message += " %s tog din plats." % eq.fadder.user.username
            except EnterQueue.DoesNotExist:
                pass

            messages.add_message(request, messages.INFO, message)

    return redirect("fadderanmalan:jobsignup_detail", job.slug)
