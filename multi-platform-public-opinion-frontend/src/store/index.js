import { createStore } from 'vuex'
import user from './modules/user'
import opinion from './modules/opinion'

export default createStore({
  modules: {
    user,
    opinion
  }
}) 