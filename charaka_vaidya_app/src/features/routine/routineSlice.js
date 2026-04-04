import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { routineAPI } from '../../app/api';

export const fetchRoutine = createAsyncThunk('routine/fetch', async (season, { rejectWithValue }) => {
  try {
    const res = await routineAPI.get(season);
    return res.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.detail || 'Failed to load routine');
  }
});

const routineSlice = createSlice({
  name: 'routine',
  initialState: {
    data: null,
    season: null,
    loading: false,
    error: null,
  },
  reducers: {
    setSeason: (state, action) => { state.season = action.payload; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchRoutine.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchRoutine.fulfilled, (state, action) => { state.loading = false; state.data = action.payload; })
      .addCase(fetchRoutine.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { setSeason } = routineSlice.actions;
export default routineSlice.reducer;
