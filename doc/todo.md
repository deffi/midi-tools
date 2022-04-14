Next steps (fake piano):
  * Add drive info
  * Add folder info
  * Handle controller change messages

Next steps (other):
  * Analyze recorded messages with parsers
  * Controller change messages:
    * Parse (the channel is encoded into the first byte)
    * Don't display?

Implementation:
  * There should be a class hierarchy:
        Message -> SysExMessage -> Yamaha50Message -> XxxMessage
