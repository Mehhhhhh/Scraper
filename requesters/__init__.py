from requesters.requester_factory import RequesterFactory

# register nasdaq requester
from requesters.nasdaq_requester import NasdaqRequester
RequesterFactory.register("nasdaq", NasdaqRequester)