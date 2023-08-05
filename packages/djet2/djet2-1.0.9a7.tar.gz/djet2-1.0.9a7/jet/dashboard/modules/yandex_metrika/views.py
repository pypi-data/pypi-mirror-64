from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from jet.dashboard.models import UserDashboardModule
from .module import YandexMetrikaClient


def yandex_metrika_grant_view(request, pk):
    client = YandexMetrikaClient()
    return redirect(client.get_oauth_authorize_url(pk))


def yandex_metrika_revoke_view(request, pk):
    try:
        module = UserDashboardModule.objects.get(pk=pk)
        module.pop_settings(('access_token', 'expires_in', 'token_type', 'counter'))
        return redirect(reverse('jet-dashboard:update_module', kwargs={'pk': module.pk}))
    except UserDashboardModule.DoesNotExist:
        return HttpResponse(_('Module not found'))


def yandex_metrika_callback_view(request):
    try:
        state = request.GET['state']
        code = request.GET['code']

        module = UserDashboardModule.objects.get(pk=state)

        client = YandexMetrikaClient()
        result, exception = client.oath_token_request(code)

        if result is None:
            messages.error(request, _('API request failed.'))
        else:
            module.update_settings(result)

        return redirect(reverse('jet-dashboard:update_module', kwargs={'pk': module.pk}))
    except KeyError:
        return HttpResponse(_('Bad arguments'))
    except UserDashboardModule.DoesNotExist:
        return HttpResponse(_('Module not found'))
