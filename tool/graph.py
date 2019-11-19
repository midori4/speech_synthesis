# -*- coding: utf-8 -*-
#音素情報付きグラフを作成

import sys, os
import argparse
import numpy
import struct
import matplotlib.pyplot as plt

#線の色を指定
color_list = ['black','red','blue','green','cyan','magenta','yellow']

def load_binary(data_file,order,target,bit,format):
    data_length = int(os.path.getsize(data_file) / bit)
    data_frame = int(data_length / order)
    with open(data_file) as file:
        #tmp = numpy.array(struct.unpack(format*data_length,file.read())).reshape(data_frame,order)[:,int(target)]
        tmp = numpy.fromfile(file,format).reshape(data_frame,order)[:,target]

    return tmp


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="時系列データを音素情報付きでグラフ化")
    
    parser.add_argument('-i','--input',type=str,required=True,nargs='*',
                        help="プロットしたい時系列データ(1つ以上)と時間情報付きラベルファイルを指定")
    parser.add_argument('-o','--output',default=None,type=str,
                        help="グラフの出力ファイルを指定．オプションがない場合はグラフを表示")
    parser.add_argument('-r','--rate',default=200.0,type=float,
                        help="時系列データのフレームレート")
    parser.add_argument('-t','--target',default='0',type=str,nargs='*',
                        help="入力した各時系列データのうちプロットする次元")
                        
    parser.add_argument('-c','--csv',action='store_true',
                        help="入力ファイルが表(csv)形式である場合")
    parser.add_argument('-f','--float',action='store_true',
                        help="入力ファイルがバイナリデータ(float型)である場合")
    parser.add_argument('-s','--short',action='store_true',
                        help="入力ファイルがバイナリデータ(short型)である場合")
    parser.add_argument('-a','--ascii',action='store_true',
                        help="入力ファイルがテキスト形式である場合")

    parser.add_argument('-m','--order',default=1,type=int,
                        help="入力した時系列データの次元数")

    parser.add_argument('-xr','--x_range',default=None,type=float,nargs=2,
                        help="x軸の範囲")
    parser.add_argument('-xl','--x_label',default=None,type=str,
                        help="x軸のラベル")
    parser.add_argument('-yr','--y_range',default=None,type=float,nargs=2,
                        help="y軸の範囲")
    parser.add_argument('-yl','--y_label',default=None,type=str,
                        help="y軸のラベル")
    parser.add_argument('-fs','--fontsize',default=12,type=float,
                        help="軸ラベルと数値のサイズ")
    parser.add_argument('-l','--legend',default=None,type=str,nargs='*',
                        help="凡例を設定")
    parser.add_argument('-lp','--legend_position',default='best',type=str,
                        help="凡例の表示位置(best,upper left,upper right,lower left,lower right,etc...)")

    parser.add_argument('-pp','--phoneme_position',default=None,type=float,
                        help="音素情報の縦方向の表示位置を指定(y軸上の値に対応)")
    parser.add_argument('-ps','--phoneme_shift',default=0.0,type=float,
                        help="各音素の横方向の表示位置を調整(値が大きいほど左に移動)")

    parser.add_argument('-xs','--xsec',action='store_true',
                        help="横軸を秒単位に(指定がない場合はフレーム単位)")

    args = parser.parse_args()
    
    #入力ファイルを時系列データとラベルファイルに割当
    data_file = args.input[:-1]
    label_file = args.input[-1]
    
    #入力時系列データ数
    num_data = len(data_file)
    
    #入力時系列データ数とプロットする次元の指定数が一致しない場合の警告
    if len(args.target) != num_data:
        sys.stdout.write("Mismatch Number of input data and target.\n")
        exit()

    #プロットするデータを抽出
    y_data = []
    for i in range(num_data):
        if args.float:
            tmp = load_binary(data_file[i],args.order,int(args.target[i]),4,'f4')
        elif args.short:
            tmp = load_binary(data_file[i],args.order,int(args.target[i]),2,'i2')
        elif args.ascii:
            tmp = numpy.loadtxt(data_file[i],delimiter=',',dtype=float)
            tmp = tmp.reshape(tmp.shape[0]/args.order,-1)[:,int(args.target[i])]
        elif args.csv:
            tmp = numpy.loadtxt(data_file[i],delimiter=',',dtype=float,skiprows=1)
            with open(data_file[i],'r') as file:
                header = file.readline().rstrip('\n').split(',')
            idx = header.index(args.target[i])
            data_frame = tmp.shape[0]
            tmp = tmp.reshape(data_frame,-1)[:,idx]
        else:
            tmp = numpy.load(data_file[i])
            data_frame = tmp.shape[0]
            tmp = tmp.reshape(data_frame,-1)[:,int(args.target[i])]
        y_data.append(tmp)
    y_data = numpy.array(y_data)

    #ラベルファイルから音素が切り替わる時間と音素の種類を取得
    partition_list = [0]
    phoneme_list = []
    with open(label_file) as file:
        for line in file:
            line = line.split()
            start = float(line[0])/10000000
            end = float(line[1])/10000000
            phoneme = line[2]
            partition_list.append(end)
            phoneme_list.append(phoneme)

    #x軸方向のデータ
    num_frame = y_data.shape[1]
    x_data = numpy.array(range(num_frame))
    if args.xsec:
        partition_list = numpy.array(partition_list)
        x_data = x_data / args.rate
    else:
        partition_list = numpy.array(partition_list) * args.rate

    fig = plt.figure()

    #各時系列データをプロット
    if args.legend is None:
        for i in range(num_data):
            plt.plot(x_data,y_data[i],color=color_list[i])
    else:
        for i in range(num_data):
            plt.plot(x_data,y_data[i],color=color_list[i],label=args.legend[i])
        #凡例の位置を指定
        #plt.legend(loc='best')
        plt.legend(loc=args.legend_position)

    #グラフ上の文字サイズを一括で変更
    #plt.rcParams["font.size"] = args.fontsize

    #目盛りの数値の文字サイズを変更
    plt.tick_params(labelsize=args.fontsize)

    #各軸のラベルを設定
    if args.x_label is not None:
        plt.xlabel(args.x_label,fontsize=args.fontsize)
    if args.y_label is not None:
        plt.ylabel(args.y_label,fontsize=args.fontsize)

    #横方向の範囲の指定と出力する音素の範囲を取得
    if args.x_range is None:
        plt.xlim([x_data[0],x_data[-1]])
        start_phoneme_id = 0
        end_phoneme_id = len(phoneme_list)
    else:
        plt.xlim([args.x_range[0],args.x_range[1]])
        start_phoneme_id = numpy.where(partition_list>=args.x_range[0])[0][0]
        end_phoneme_id = numpy.where(partition_list>=args.x_range[1])[0][0]-1

    #縦方向の範囲の指定
    if args.y_range is not None:
        plt.ylim([args.y_range[0],args.y_range[1]])

    #出力する音素の位置を指定
    if args.phoneme_position is None:
        phoneme_position = max(y_data.reshape(-1))
    else:
        phoneme_position = args.phoneme_position

    #音素の仕切り線を黒の点線(black,dashed)で出力
    for id in range(len(partition_list)-1):
        plt.axvline(x=partition_list[id],color='black',linestyle='dashed')

    #音素の種類を出力
    for id in range(start_phoneme_id,end_phoneme_id):
        plt.text((partition_list[id]+partition_list[id+1])/2-len(phoneme_list[id])*args.phoneme_shift,
                 phoneme_position,phoneme_list[id])

    #グラフの出力(表示or保存)
    if args.output is None:
        plt.show()
    else:
        plt.savefig(args.output)


