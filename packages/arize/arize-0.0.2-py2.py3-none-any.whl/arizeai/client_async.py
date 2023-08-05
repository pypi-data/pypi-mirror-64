import random
import time
from api import AsyncAPI

CALLS = 100_000

arize = AsyncAPI(account_id=1234)

lable = {}
for i in range(100):
    lable['label_{}'.format(i)] = 'value_{}'.format(i)

start = time.time() * 1000
for i in range(CALLS):
    arize.log(
        model_id='sample-model-v'+ str(int(random.random()*10)),
        prediction_id='abc_'+ str(int(random.random()*CALLS)),
        prediction_value=True,
        labels=lable
    )
end = time.time() * 1000
print('process took {}ms'.format(end-start))
