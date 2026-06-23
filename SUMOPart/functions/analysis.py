import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def getCSVFileName(vehicles):
    return '/all_sums_'+str(vehicles)+'.csv'

def get_fazes_folder(gridsDataFolder, green_faze = 30, red_faze = 30, withModel = False):
    folderTypeRun = "default/" if withModel == False else "predict/"
    return gridsDataFolder+folderTypeRun+"fazes_g"+str(green_faze)+"r_"+str(red_faze)


def get_dataFolder(gridsDataFolder, vehicles, green_faze = 30, red_faze = 30, withModel=False):
    return get_fazes_folder(gridsDataFolder, green_faze, red_faze, withModel)+"/dataFor_"+str(vehicles)+"_vehicles"

def get_csvFazesPath(dataFolder, curCount):
    return dataFolder + getCSVFileName(curCount)

def plots(vehicles, pathToSave, green_faze = 30, red_faze = 30, withModel = False):
    vel=np.zeros(len(vehicles))
    nc=np.zeros(len(vehicles))
    flux=np.zeros(len(vehicles))
    save_imgs_folder = get_fazes_folder(pathToSave, green_faze, red_faze, withModel)
    for i in range(0,len(vehicles)):
        cur_count = vehicles[i]
        data_folder = get_dataFolder(pathToSave, cur_count, green_faze, red_faze, withModel)
        txt=np.loadtxt(data_folder+'/velm'+str(cur_count)+'.txt')
        nc[i] = np.mean(txt[95:100, 0])
        vel[i] = np.mean(txt[95:100, 1])
        flux[i]=np.mean(txt[95:100,2])
        # print(nc[i],vel[i],flux[i])

    # fig=plt.figure()
    plt.plot(nc/3000,vel,'o')
    plt.plot(nc / 3000, vel, color='k')
    plt.xlabel('Density')
    plt.ylabel('Velocity')
    plt.title('Скорость к плотности')
    plt.tight_layout()
    plt.savefig(save_imgs_folder+'/vel-density.png',dpi=600)

    fig=plt.figure()
    # Поток (flux) измеряет количество автомобилей, проходящих через определённую точку за конкретное время, 
    # — мера пропускной способности.
    plt.plot(nc / 3000,flux,'o',label='Traffic Simulation')
    plt.plot(nc / 3000, flux, color='k')
    plt.plot(vehicles/3000,vehicles*vel[0],'r--',label='No Interaction')
    plt.ylim(0,2800)
    plt.legend()
    plt.xlabel('Density')
    plt.ylabel('Flux')
    plt.title('Поток к плотности')
    plt.tight_layout()
    plt.savefig(save_imgs_folder+'/flux-density.png', dpi=600)
    
    plt.tight_layout() # Prevents label overlapping
    plt.show()

def plots_mean_traffic(durations, vehicles, pathToSave, withModel = False):
    col_names = np.insert(np.array(vehicles).astype(str), 0, "duration") 
    # Create the DataFrame
    dfAll = pd.DataFrame(columns=col_names)

    for duration in durations:
        duration_mean_array = []
        for i in range(0,len(vehicles)):
            cur_count = vehicles[i]
            data_folder = get_dataFolder(pathToSave, cur_count, green_faze=duration, red_faze=duration, withModel=withModel)
            df = pd.read_csv(data_folder + getCSVFileName(cur_count))
            duration_mean_array.append(df.iloc[0].mean())
        new_array = np.array(duration_mean_array)
        dfAll = pd.concat([dfAll, pd.DataFrame([np.insert(new_array, 0, duration)], columns=dfAll.columns)],
                           ignore_index=True)
    print(dfAll)
    dfAll.set_index('duration').plot(ylabel='Mean машин, проехавших через светофор', xlabel='Продолжительность сигнала светофора', marker='o')
    plt.savefig(pathToSave+'/vehicles_passed_mean.png', dpi=600)
    plt.show()

def getRunInfoFileName(vehicles_count, phaseDuration, withModel = False):
    postfix = 'predict' if withModel else 'default'
    return f"runInfo_v{vehicles_count}_g{phaseDuration}_{postfix}.csv"

def getRunInfoPath(vehicles_count, phaseDuration, withModel = False):
    parentFolder = 'predict_runs/' if withModel else 'default_runs/'
    
    return parentFolder + getRunInfoFileName(vehicles_count, phaseDuration, withModel)

def plotTidLineGraf(allInfoDF, tlsId, column, columnLabel, title):
    '''Отрисовывает график по столбику для определенного Светофора'''
    # Фильтруем данные с tlsId
    id_begin = f"{tlsId}_veh"
    df_b1 = allInfoDF[allInfoDF['tls_id'].str.contains(id_begin, na=False)]

    # Извлекаем veh_count и постфикс
    df_b1['veh_count'] = df_b1['tls_id'].str.extract(rf'{id_begin}_(\d+)').astype(int)
    df_b1['postfix'] = df_b1['tls_id'].str.extract(rf'{id_begin}_\d+_(.+)')
    df_b1 = df_b1.sort_values('veh_count')

    # Уникальные постфиксы (для уникальных режимов)
    unique_postfixes = df_b1['postfix'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_postfixes)))
    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h']

    plt.figure(figsize=(14, 7))

    # Группируем по постфиксу
    for i, postfix in enumerate(unique_postfixes):
        data = df_b1[df_b1['postfix'] == postfix].sort_values('veh_count')
        
        # Рисуем линию с маркерами одного цвета и типа
        plt.plot(data['veh_count'], data[column], 
                        marker=markers[i % len(markers)], 
                        color=colors[i],
                        label=f'{postfix}', 
                        linewidth=2, 
                        markersize=10,
                        linestyle='-')
        
        # Добавляем значения на точки с указанием полного tls_id
        for x, y in zip(data['veh_count'], data[column]):
            plt.text(x, y + max(df_b1[column]) * 0.02, 
                    f'{int(y)}', ha='center', va='bottom', fontsize=10, rotation=45)

    plt.xlabel('Количество автомобилей в симуляции', fontsize=12)
    plt.ylabel(columnLabel, fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10, title='Режим')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(sorted(df_b1['veh_count'].unique()), fontsize=10)
    plt.tight_layout()
    plt.show()