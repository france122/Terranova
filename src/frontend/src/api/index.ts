import client from './client';

export const auth = {
  register: (username: string, password: string) =>
    client.post('/auth/register', { username, password }),
  login: (username: string, password: string) =>
    client.post('/auth/login', { username, password }),
  me: () => client.get('/auth/me'),
};

export const graph = {
  getDomains: () => client.get('/graph/domains'),
  getDomainMap: (domainId: string) => client.get(`/graph/map/${domainId}`),
  getNode: (nodeId: string) => client.get(`/graph/node/${nodeId}`),
};

export const mapApi = {
  getMapState: (domainId: string) =>
    client.get('/map/state', { params: { domain_id: domainId } }),
};

export const learn = {
  completeNode: (nodeId: string) =>
    client.post('/learn/complete', { node_id: nodeId }),
  rateNode: (nodeId: string, stars: number) =>
    client.post('/learn/rate', { node_id: nodeId, stars }),
};

export const quest = {
  getDailyQuests: () => client.get('/quests/daily'),
  getChallenges: () => client.get('/quests/challenges'),
  completeQuest: (questId: number) => client.post(`/quests/${questId}/complete`),
};

export const achievement = {
  getAchievements: () => client.get('/achievements/'),
};

export const social = {
  getLeaderboard: (type: string) => client.get(`/social/leaderboard/${type}`),
  addFriend: (username: string) =>
    client.post('/social/friends/add', { username }),
  getFriendsProgress: (domainId: string) =>
    client.get('/social/friends/progress', { params: { domain_id: domainId } }),
};
