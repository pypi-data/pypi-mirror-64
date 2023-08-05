import logging
log = logging.getLogger("[validium]")
log.addHandler(logging.NullHandler()) # ignore log messages by defualt

class Validator:

  def __init__(self, predicate, msg=None):

    assert callable(predicate), "the argument 'predicate' must be callable"
    assert msg is None or isinstance(msg, str), "the argument 'msg' must be None or an instance of str"

    self.__dict__ = dict(
      predicate=predicate,
      msg=msg,
    )

  def validate(self, target, tag=None):
    assert self.confirm(target, tag), self.msg

  def confirm(self, target, tag=None):
    result = self.predicate(target)
    t = tag if tag is not None else repr(target)
    log.info(f"💎({t}) - {'✅ pass' if result else '❌ fail'}: {self.msg}")
    
    return result