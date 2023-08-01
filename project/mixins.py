from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect


class CustomUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().owner
    

class NotLoggedMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('index'))
        return super().dispatch(request, *args, **kwargs)