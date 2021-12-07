from nmastudio.nmastudio import *
from nmastudio.tools.utils import _IS_JUPYTER

if _IS_JUPYTER:
    from IPython.core.display import HTML
    with open(f'nmastudio/__res/icon_tiny.svg', 'r') as f:
        _svg_cnn = f.read()
    html_repr = _svg_cnn + f"""</br>
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
    display(HTML(html_repr))