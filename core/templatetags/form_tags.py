from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='addclass')
def addclass(field, css_class):
    """添加 CSS 类和 placeholder 到表单字段"""
    attrs = {
        "class": css_class,
        "placeholder": "输入要发送的消息..."
    }
    return field.as_widget(attrs=attrs)

@register.filter(name='addattr')
def addattr(field, attr_string):
    """添加属性到表单字段"""
    try:
        attr_name, attr_value = attr_string.split(':')
        widget = field.as_widget(attrs={attr_name: attr_value})
        return mark_safe(widget)
    except (ValueError, AttributeError):
        return field 