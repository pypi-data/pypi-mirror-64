from neon_goby.clean import clean
from neon_goby.split import split

class NeonGoby(object):
  @staticmethod
  def parse(text, anonymous=True):
    return split(clean(text, anonymous=anonymous))
