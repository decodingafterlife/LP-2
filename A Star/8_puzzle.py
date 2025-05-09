import heapq
import copy

N=3
row=[1,0,-1,0]
col=[0,-1,0,1]

def misplaced_tiles(state, goal):
    return sum(state[i][j] != 0 and state[i][j] != goal[i][j] for i in range(N) for j in range(N))

def isSafe(x,y):
    return 0<=x<N and 0<=y<N

def matrix_to_tuple(mat):
    return tuple(tuple(row) for row in mat)


def solve(initial, goal):

    def find_zero(mat):
        for i in range(N):
            for j in range(N):
                if(mat[i][j] == 0):
                    return i, j
                
    x, y = find_zero(initial)
    pq=[]
    visited = set()

    heapq.heappush(pq, (misplaced_tiles(initial, goal), 0, initial, x, y))
    visited.add(matrix_to_tuple(initial))

    k = 1
    while pq:

        f,g,mat,x,y = heapq.heappop(pq)

        print(f"Step {k}: g = {g}  h = {f-g} f={f}")
        for row_mat in mat:
            print(row_mat)
        print()
        k += 1
        if misplaced_tiles(mat, goal) == 0:
            print("Goal Reached !")
            return


        for i in range(4):

            nx, ny = x+row[i], y+col[i]

            if(isSafe(nx, ny)):

                new_mat = copy.deepcopy(mat)
                new_mat[x][y], new_mat[nx][ny] = new_mat[nx][ny], new_mat[x][y]
                new_mat_tuple = matrix_to_tuple(new_mat)

                if new_mat_tuple not in visited:
                    visited.add(new_mat_tuple)
                    h = misplaced_tiles(new_mat, goal)
                    heapq.heappush(pq, (g+1+h, g+1, new_mat, nx, ny))


initial = [
    [1, 2, 3],
    [4, 5, 6],
    [0, 7, 8]
]

goal = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]

solve(initial, goal)