import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { chatAPI } from '../../app/api';

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async ({ query, history, simple_mode, language }, { rejectWithValue }) => {
    try {
      const res = await chatAPI.send(query, history, simple_mode, language);
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'Failed to get response');
    }
  }
);

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [],
    sources: [],
    loading: false,
    error: null,
    simpleMode: false,
  },
  reducers: {
    addUserMessage: (state, action) => {
      state.messages.push({ role: 'user', content: action.payload });
    },
    clearChat: (state) => {
      state.messages = [];
      state.sources = [];
    },
    toggleSimpleMode: (state) => {
      state.simpleMode = !state.simpleMode;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false;
        state.messages.push({ role: 'assistant', content: action.payload.answer, meta: action.payload });
        state.sources = action.payload.sources || [];
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { addUserMessage, clearChat, toggleSimpleMode } = chatSlice.actions;
export default chatSlice.reducer;
