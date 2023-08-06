from django.contrib.admin import ModelAdmin
from django.contrib import messages
from collections import OrderedDict
import inspect
from django.core.paginator import Paginator, EmptyPage, InvalidPage


class SimulatedInlinesModelAdmin(ModelAdmin):
    """
    Class to add custom inlines to the model admin templates,

    extends the interface with a "simulated_inlines" atribute that should
    contain a tuple or list of "SimulatedInline" classes
    """

    change_form_template = "admin/django_simulated_inlines/change_form.html"

    class Media:
        js = ("django_simulated_inlines/js/django_simulated_inlines.js",)

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}

        button_class, button_method = self._check_button_pressed(request)

        s_inlines_context = []
        if self.simulated_inlines:
            show = True
            queryset = self.get_queryset(request)
            self.s_inlines_instances = [inline() for inline in self.simulated_inlines]
            for s_inline in self.s_inlines_instances:
                inline_context = s_inline.to_context(request, object_id, queryset)
                s_inlines_context.append(inline_context)

                # execute the button if provided
                if button_class and s_inline.__class__.__name__.lower() == button_class:
                    s_inline._handle_button(button_method, request, object_id)

        extra_context["simulated_inlines"] = {
            "show": show,
            "inlines": s_inlines_context,
        }

        return super(SimulatedInlinesModelAdmin, self).changeform_view(
            request, object_id, form_url, extra_context
        )

    def _check_button_pressed(self, request):
        button_pressed = request.GET.get("button")
        class_name = None
        method_name = None
        if button_pressed and "__" in button_pressed:
            class_name, method_name = button_pressed.split("__")

        return class_name, method_name


class SimulatedInline(object):
    """
    To be used in SimulatedInlinesModelAdmin classes,
    this shares as much as possible the interface with
    the existing admin inlines
    """

    template = "admin/django_simulated_inlines/list.html"
    per_page = None
    collapse = False
    subtitle = None
    outer_description = None
    buttons = []

    def __init__(self):
        # TODO chekc self.model and self.fields (see how django hadles this)

        original_attrs = self.model._meta.original_attrs
        if not self.verbose_name:
            self.verbose_name = original_attrs.verbose_name

        if not self.verbose_name_plural:
            self.verbose_name_plural = original_attrs.verbose_name_plural

        self._translate_fields()

    def _translate_fields(self):
        """Translates the asked fields to _field_map with links"""
        self._field_map = OrderedDict()
        try:
            model_name_map = self.model._meta._name_map
        except AttributeError:
            model_name_map = self._map_model_fields_to_names()

        for field in self.fields:
            field_name = field
            link = None
            field_for_link = None

            if isinstance(field, tuple):
                field_name = field[0]
                if len(field) == 2:
                    field_name, link = field
                    field_for_link = "id"
                if len(field) == 3:
                    field_name, link, field_for_link = field

            class_methods = inspect.getmembers(self, predicate=inspect.ismethod)
            method = [m for f, m in class_methods if field_name == f]
            if method:
                self._field_map[field_name] = {
                    "method": method[0],
                    "label": method[0].short_description,
                    "link": link,
                    "field_for_link": field_for_link,
                }
            elif field_name in model_name_map:
                model_field = model_name_map[field_name][0]
                self._field_map[field_name] = {
                    "method": None,
                    "label": model_field.verbose_name,
                    "link": link,
                    "field_for_link": field_for_link,
                }
            else:
                # TODO: don't allow (check how django does this)
                pass

    def _map_model_fields_to_names(self):
        fields = {}
        for field in self.model._meta.fields:
            fields[field.name] = (field,)
        return fields

    def _get_label(self, field):
        return self._field_map[field]["label"].capitalize()

    def _paginate(self, request, object_id=None, parent_queryset=None):
        # filter parent queryset to object
        if object_id and parent_queryset:
            parent_queryset = parent_queryset.filter(pk=object_id)
        qs = self.get_queryset(request, object_id, parent_queryset)

        page = None
        page_num = None
        if self.per_page:
            paginator = Paginator(qs, self.per_page)
            try:
                param_name = self.__class__.__name__.lower() + "-page"
                page_num = int(request.GET.get(param_name, "1"))
            except ValueError:
                page_num = 1

            try:
                page = paginator.page(page_num)
            except (EmptyPage, InvalidPage):
                page = paginator.page(paginator.num_pages)

            qs = page.object_list

        return qs, page, page_num

    def _get_classes(self):
        collapse_class = "collapse-simulated-inline" if self.collapse else ""
        return collapse_class

    def _get_buttons(self):
        buttons = []
        if self.buttons:
            class_methods = inspect.getmembers(self, predicate=inspect.ismethod)
            class_buttons = [(n, b) for n, b in class_methods if n in self.buttons]
            # TODO: validate the button function exists
            for method_name, button in class_buttons:
                full_name = "%s__%s" % (self.__class__.__name__, method_name)
                buttons.append((button.short_description, full_name.lower()))
        return buttons

    def get_subtitle(self, request, object_id):
        """Override this to customize the subtitle"""
        return self.subtitle

    def get_queryset(self, request, object_id=None, parent_queryset=None):
        """
        Gets all model values by default, override this to add filters
        ps: the object_id and queryset refers to the parent of the inline
        """
        return self.model.objects.all()

    def to_context(self, request, object_id=None, parent_queryset=None):
        """
        Creates the expected context to be appended to the template
        ps: the object_id and queryset refers to the parent of the inline
        """
        qs, page, page_num = self._paginate(request, object_id, parent_queryset)

        return {
            "name": self.__class__.__name__.lower(),
            "classes": self._get_classes(),
            "template": self.template,
            "verbose_name": self.verbose_name_plural.upper(),
            "table_headers": map(self._get_label, self._field_map),
            "rows": map(self.serialize, qs),
            "page_num": page_num,
            "page_obj": page,
            "buttons": self._get_buttons(),
            "subtitle": self.get_subtitle(request, object_id),
        }

    def serialize(self, obj):
        """Serializes all the fields in a row"""
        row = []
        for field, field_data in self._field_map.items():
            link = field_data.get("link")
            field_for_link = field_data.get("field_for_link")
            method = field_data.get("method")

            if link and "%s" in link and field_for_link:
                link_value = getattr(obj, field_data.get("field_for_link"))
                if link_value:
                    link = str(link) % link_value
                else:
                    link = None

            text = method(obj) if method else str(getattr(obj, field, None))

            row.append({"label": field_data.get("label"), "text": text, "link": link})
        return row

    def _handle_button(self, button_name, request, object_id):
        try:
            getattr(self, button_name)(request, object_id)
        except Exception:
            messages.error(request, "Could not execute %s button" % button_name)
