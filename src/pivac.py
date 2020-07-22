import pifaceio, time

pf = pifaceio.PiFace()

pin_vals = 0

pin_current = 0
pin_change = False

pin_ctr = [0, 0]
pin_last = [None, None]
pin_val = [0, 0]

ITERATION_DELAY = 0.01
ITERATION_COUNT = 5
iterations = ITERATION_COUNT - 1
iteration_cnt_flag = iterations - 1

relay_on = False
relay_tmp_val = False
valid_change = False

while True:

    pin_vals = pf.read()
    
    for idx in range(2):

        pin_val[idx] = pin_vals & (idx + 1)
        bit_set = pow(2, idx)

        if pin_last[idx] != pin_val[idx]:
            pin_ctr[idx] = 0
            pin_last[idx] = pin_val[idx]

        else:
            if pin_val[idx] and pin_ctr[idx] <= iteration_cnt_flag:
                pin_ctr[idx] = pin_ctr[idx] + 1

            if (pin_ctr[idx] >= iterations):
                pin_change = True
                if idx == 0:
                    relay_tmp_val = 1
                else:
                    relay_tmp_val = 0

    if pin_change:
        if relay_tmp_val == 1 and not relay_on:
            relay_on = True
            pf.write(1)
            valid_change = True
        else:
            if relay_tmp_val == 0 and relay_on:
                relay_on = False
                pf.write(0)
                valid_change = True

        if valid_change:
            print('Relay On:', relay_on)
            valid_change = False

        pin_change = False

    time.sleep(ITERATION_DELAY)
