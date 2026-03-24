import { configureStore } from '@reduxjs/toolkit';
import chatReducer from '../features/chat/chatSlice';
import herbsReducer from '../features/herbs/herbsSlice';
import doshaReducer from '../features/dosha/doshaSlice';
import routineReducer from '../features/routine/routineSlice';
import samhitaReducer from '../features/samhita/samhitaSlice';
import healthReducer from '../features/health/healthSlice';

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    herbs: herbsReducer,
    dosha: doshaReducer,
    routine: routineReducer,
    samhita: samhitaReducer,
    health: healthReducer,
  },
});

export default store;
