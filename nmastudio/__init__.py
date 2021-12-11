from nmastudio.nmastudio import *
from nmastudio.tools.utils import _IS_JUPYTER
import sys

# print(locals()['__spec__'].origin)

with open(f'nmastudio/__res/icon_mini.svg', 'r') as f:
    _svg_cnn = f.read()
HTML_repr_extended = _svg_cnn + f"""
<span style="white-space: nowrap;">
<b>NMA Studio</b>

</span></br>
<span style="white-space: nowrap;">
<span style="color: gray">Interactive app:</span>
<span white-space: nowrap;><a  href="www.nmastudio.com">www.nmastudio.com</a></span>
</span></br>
<span style="white-space: nowrap;">
<span style="color: gray">Documentation
<span white-space: nowrap;><a href="https://github.com/silviametelli/nmastudio">available here</a>.</span></span>
</span></br>
"""

PLAIN_repr_extended = """My personalised representation of nmastudio"""

# if _IS_JUPYTER:
#     from IPython.core.display import HTML
#     display(HTML(_svg_cnn))

class CustomReprModule(nmastudio.__class__):
    def __init__(self, other):
        for attr in dir(other):
            setattr(self, attr, getattr(other, attr))
    def __repr__(self):
        return PLAIN_repr_extended
    def _repr_html_(self):
        return HTML_repr_extended

# THIS MUST BE THE LAST LINE!
sys.modules[__name__] = CustomReprModule(sys.modules[__name__])