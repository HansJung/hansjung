# -*- coding: utf-8 -*-

'''
그래프 짜는거 새로짜기
'''

def adaptive_thr(data, initial_info):
    def check_cross(prev_thr, prev_sig, cur_thr, cur_sig):
        if prev_thr > prev_sig:
            if cur_thr < cur_sig:
                return True
                # 크로스포인트는 과거와 현재 사이에 찍힌다.
                # 즉, 현재포인트부터 신호를 받는게 좋다.
            else: # cur_thr > cur_sig
                return False
        else:
            return False

    mymax = {}
    mysignal = data
    slope = initial_info[1]
    start = initial_info[0]
    adap = [start]
    mode = 'thr'
    cross = False
    x = 1

    for idx in range(len(mysignal)):
        # 모드 : sig, thr
            # thr 모드 : 직선을 타고 내려간다.
            # sig 모드 : 신호를 타고 올라간다.

        # 알고리즘
            # 시작은 thr모드
                # 기울기0, 스타트0 으로 직선을 그린다.
                # 교차인지 확인
                    # 만일 교차가 아니라면 계속 thr모드로 진행
                    # 교차면 sig모드 변환
                    # 다음 iteration
            # sig모드이면
                # increasing 이면 타고 올라간다.
                # decreasing 이면 thr 모드 변환
                    # 현재의 신호 포인트를 맥스로 저장
                    # slope은 그대로
                    # start는 맥스
                    # 새로운 x를 잡아서 진행한다.
                # 다음 iteration

        # MODE CHECK
        if idx > 0:
            prev_thr = adap[len(adap)-2]
            cur_thr = adap[len(adap)-1]
            prev_sig = mysignal[idx-1]
            cur_sig = mysignal[idx]
            cross = check_cross(prev_thr,prev_sig,cur_thr,cur_sig)
        else:
            pass

        if mode == 'thr':
            if cross == False:
                mode = 'thr'
                adap.append(start + x * slope)
                x += 1

            elif cross == True:
                mode = 'sig'
                adap.append(cur_sig )
                continue

        elif mode == 'sig':
            if cur_sig > prev_sig:
                adap.append(cur_sig)
            if cur_sig < prev_sig:
                adap.append(cur_sig)
                mode = 'thr'
                mymax.update( {idx : prev_sig}  )
                start = prev_sig
                x = 0
                continue
    return [adap, mymax]


def main():
    def mydata():
        from data_call import data_call
        testnum = 6
        mysignal = data_call("ECG_HE", testnum, 0)
        return testnum, mysignal

    def check_cross(prev_thr, prev_sig, cur_thr, cur_sig):
        if prev_thr > prev_sig:
            if cur_thr < cur_sig:
                return True
                # 크로스포인트는 과거와 현재 사이에 찍힌다.
                # 즉, 현재포인트부터 신호를 받는게 좋다.
            else: # cur_thr > cur_sig
                return False
        else:
            return False


    def adaptive_thr():
        import numpy as np
        testnum, mysignal = mydata()
        mymax = {}

        # 우리가 가진 수식들.
        Vold = 0 # V{n-1}
        Vnew = 0 # V{n}
        Fs = 75  # Sampling Frequency
        StdPPG = np.std(mysignal)
        slope_old = 0
        slope_new = 0


        slope = -0.75
        start = 100
        adap = [start]
        mode = 'thr'
        cross = False
        x = 1

        for idx in range(len(mysignal)):
            # 모드 : sig, thr
                # thr 모드 : 직선을 타고 내려간다.
                # sig 모드 : 신호를 타고 올라간다.

            # 알고리즘
                # 시작은 thr모드
                    # 기울기0, 스타트0 으로 직선을 그린다.
                    # 교차인지 확인
                        # 만일 교차가 아니라면 계속 thr모드로 진행
                        # 교차면 sig모드 변환
                        # 다음 iteration
                # sig모드이면
                    # increasing 이면 타고 올라간다.
                    # decreasing 이면 thr 모드 변환
                        # 현재의 신호 포인트를 맥스로 저장
                        # slope은 그대로
                        # start는 맥스
                        # 새로운 x를 잡아서 진행한다.
                    # 다음 iteration

            # MODE CHECK
            if idx > 0:
                prev_thr = adap[len(adap)-2]
                cur_thr = adap[len(adap)-1]
                prev_sig = mysignal[idx-1]
                cur_sig = mysignal[idx]
                cross = check_cross(prev_thr,prev_sig,cur_thr,cur_sig)
            else:
                pass

            if mode == 'thr':
                if cross == False:
                    mode = 'thr'
                    adap.append(start + x * slope)
                    x += 1

                elif cross == True:
                    mode = 'sig'
                    adap.append(cur_sig )
                    continue

            elif mode == 'sig':
                if cur_sig > prev_sig:
                    adap.append(cur_sig)
                if cur_sig < prev_sig:
                    adap.append(cur_sig)
                    mode = 'thr'
                    mymax.update( {idx : prev_sig}  )
                    start = prev_sig
                    x = 0
                    continue
        return adap, mymax

    def plotting():
        import matplotlib.pyplot as plt

        adap, mymax = adaptive_thr()
        testnum, mysignal = mydata()

        #for key in sorted(mymax):
        #    plt.plot(key, mymax[key],'ro')


        plt.plot(mysignal)
        #plt.plot(adap)
        plt.xlabel("X index (1 data point every 1/75 sec.)")
        plt.ylabel("Scale modified Voltage value")
        plt.title("#" + str(testnum) + " Samples from Kiwook")

        plt.show()


    plotting()






if __name__ == "__main__":
    main()