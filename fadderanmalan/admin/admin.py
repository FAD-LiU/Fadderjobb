from django.contrib import admin, messages
from django.http import HttpResponseRedirect

from fadderanmalan.models import Type, EnterQueue, LeaveQueue, Job, Equipment, EquipmentOwnership
from .actions import job_set_locked, job_set_hidden, equipment_ownership_set_returned

from fadderjobb.filters import DropdownFilterRelated


class UsersInline(admin.TabularInline):
    verbose_name = "User"
    verbose_name_plural = "Users"

    model = Job.users.through

    extra = 0


class LQInline(admin.TabularInline):
    verbose_name = "Leavequeue"
    verbose_name_plural = "Leavequeue"

    model = LeaveQueue


class EQInline(admin.TabularInline):
    verbose_name = "Enterqueue"
    verbose_name_plural = "EnterQueue"

    model = EnterQueue


class JobAdmin(admin.ModelAdmin):
    model = Job

    inlines = (
        UsersInline,
        LQInline,
        EQInline
    )

    list_display = ("name", "date", "locked", "signed_up")

    exclude = ("users",)

    actions = (job_set_locked, job_set_hidden)

    list_filter = ("locked", "types", ("date", admin.AllValuesFieldListFilter))

    search_fields = ("name",)

    change_form_template = "admin/fadderanmalan/change_job.html"

    def signed_up(self, obj):
        return ", ".join([user.username for user in obj.users.all()])

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Sökbara fält: jobb-namn.'})

        return super(JobAdmin, self)\
            .changelist_view(request, extra_context=extra_context)

    def response_change(self, request, obj):
        if "_dequeue" in request.POST:
            if obj.full():
                messages.add_message(request, messages.ERROR, "Job is full.")
            else:
                added = obj.dequeue()
                added = [user.username for user in added]

                if len(added) > 0:
                    messages.add_message(request, messages.INFO, "Users '%s' dequeued." % "', '".join(added))
                else:
                    messages.add_message(request, messages.ERROR, "No users to dequeue.")

            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class EnterQueueAdmin(admin.ModelAdmin):
    model = EnterQueue

    list_display = ("job", "user")

    search_fields = ("user__username", "job__name")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Sökbara fält: liu-id, jobb-namn.'})

        return super(EnterQueueAdmin, self)\
            .changelist_view(request, extra_context=extra_context)


class LeaveQueueAdmin(admin.ModelAdmin):
    model = LeaveQueue

    list_display = ("job", "user")

    search_fields = ("user__username", "job__name")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Sökbara fält: liu-id, jobb-namn.'})

        return super(LeaveQueueAdmin, self)\
            .changelist_view(request, extra_context=extra_context)


class EquipmentAdmin(admin.ModelAdmin):
    model = Equipment

    list_display = ("name", "size")


class EquipmentOwnershipAdmin(admin.ModelAdmin):
    model = EquipmentOwnership

    list_display = ("name", "size", "fadder", "job", "returned")

    actions = (equipment_ownership_set_returned,)

    search_fields = ("fadder__username", "job__name")

    list_filter = (("equipment", DropdownFilterRelated), "returned")

    def get_changeform_initial_data(self, request):
        try:
            last = EquipmentOwnership.objects.latest("dispensed_at")

            return {"job": last.job}
        except EquipmentOwnership.DoesNotExist:
            return {}

    def render_change_form(self, request, context, *args, **kwargs):
        context.update({'help_text': ''})

        return super(EquipmentOwnershipAdmin, self)\
            .render_change_form(request, context, *args, **kwargs)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'help_text': 'Sökbara fält: liu-id, jobb-namn.'})

        return super(EquipmentOwnershipAdmin, self)\
            .changelist_view(request, extra_context=extra_context)

    def name(self, obj):
        return obj.equipment.name

    def size(self, obj):
        return obj.equipment.size


admin.site.register(Type)
admin.site.register(EnterQueue, EnterQueueAdmin)
admin.site.register(LeaveQueue, LeaveQueueAdmin)

admin.site.register(Job, JobAdmin)

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentOwnership, EquipmentOwnershipAdmin)
