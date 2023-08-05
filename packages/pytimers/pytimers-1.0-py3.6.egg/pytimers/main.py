import logging

from decorator_timer import DecoratorTimer, DecoratedCallable
from function import FunctionTimer, function_timer


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


@function_timer
def f(x):
    print(x)


@FunctionTimer()
def g(x):
    print(x)


if __name__ == '__main__':
    f('test')
    g('test2')

    a = DecoratorTimer()
