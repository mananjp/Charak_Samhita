import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { samhitaAPI } from '../../app/api';

export const searchSamhita = createAsyncThunk(
  'samhita/search',
  async ({ query, top_k = 5, sthana = null }, { rejectWithValue }) => {
    try {
      const res = await samhitaAPI.search(query, top_k, sthana);
      return res.data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'Search failed');
    }
  }
);

const samhitaSlice = createSlice({
  name: 'samhita',
  initialState: {
    results: [],
    query: '',
    loading: false,
    error: null,
  },
  reducers: {
    setQuery: (state, action) => { state.query = action.payload; },
    clearResults: (state) => { state.results = []; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(searchSamhita.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(searchSamhita.fulfilled, (state, action) => {
        state.loading = false;
        // May be array or object with results key
        state.results = Array.isArray(action.payload) ? action.payload : (action.payload.results || []);
      })
      .addCase(searchSamhita.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { setQuery, clearResults } = samhitaSlice.actions;
export default samhitaSlice.reducer;
