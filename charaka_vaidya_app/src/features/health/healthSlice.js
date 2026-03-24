import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { healthAPI } from '../../app/api';

export const checkHealth = createAsyncThunk('health/check', async (_, { rejectWithValue }) => {
  try {
    const res = await healthAPI.check();
    return res.data;
  } catch (err) {
    return rejectWithValue('Backend offline');
  }
});

const healthSlice = createSlice({
  name: 'health',
  initialState: { status: 'unknown', data: null, loading: false },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(checkHealth.pending, (state) => { state.loading = true; state.status = 'checking'; })
      .addCase(checkHealth.fulfilled, (state, action) => { state.loading = false; state.status = 'online'; state.data = action.payload; })
      .addCase(checkHealth.rejected, (state) => { state.loading = false; state.status = 'offline'; });
  },
});

export default healthSlice.reducer;
