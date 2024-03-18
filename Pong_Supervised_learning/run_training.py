from agent import Agent
from environment import PongEnv
import pandas as pd
import pygame

import warnings
warnings.filterwarnings('ignore')

train_mode = True
render_mode = False
path_load_model = 'model_lv1.pkl'
path_save_model = 'model.pkl'
game_speed = 100

env = PongEnv()

agent = Agent()
#agent.load_model(path_load_model)

ep_count = 0
max_episodes = 20000
results = [0] * 100
df = pd.DataFrame(columns=['vel_x', 'vel_y', 'pos_x', 'pos_y', 'pos_paddle', 'action']) 
df_temp = pd.DataFrame(columns=['vel_x', 'vel_y', 'pos_x', 'pos_y', 'pos_paddle', 'action'])

action = 0 
if train_mode:
    steps_to_train = 5 # number of episodes until retraining 
else:
    steps_to_train = 1
    
while ep_count < max_episodes: # training loop
    
    state = env.reset()
    y_paddle_list = []
    y_ball_list = []
    best_action_list = []
    df_temp = df_temp.iloc[0:0]   
    
    if render_mode:
        screen = pygame.display.set_mode((700,500))
        
    while True: # episode loop
        if ep_count > steps_to_train:
            action = agent.predict([state[:-1]])
            
        if render_mode:
            env.render(screen, game_speed)
        
        state, y_paddle, y_ball, done, atention = env.step(action)
        
        if atention == 1:
            steps_considerados =+ 1
            df_temp.loc[len(df_temp)] = state
            y_paddle_list.append(y_paddle)

        if done:
            break
        

    final_ball_pos = y_ball
    final_paddle_pos = y_paddle
    
    
    if abs(final_ball_pos - (final_paddle_pos + 50)) < 50: 
        results.pop(0)
        results.insert(len(results), 1)   #  correct action
    else:
        results.pop(0)
        results.insert(len(results), 0)   #  wrong action
        
    
    
    for i in range(len(y_paddle_list)):   # discovering best action for each step
        
        if y_paddle_list[i] + 50 < final_ball_pos:
            best_action_list.append(1)     # move Down
            
        elif y_paddle_list[i] + 50 > final_ball_pos:
            best_action_list.append(2)     # move Up

        else:
            best_action_list.append(0)     # stay there
            
 
    df_temp['action'] = best_action_list

    df = pd.concat([df_temp, df]).astype('int')
    
    df = df.drop_duplicates()
    
    if ep_count % steps_to_train == 0:
        print(f'episodio {ep_count}')
        print(f'Resultado: {sum(results)/len(results)*100} %')
        
        if train_mode:
            agent.train(df.iloc[:,:-1], df['action'])
            agent.save_model(path_save_model)
            df.to_csv('table.csv')
        
    ep_count += 1