(ns aoc.pathfinding
  "Pathfinding and search algorithms for Advent of Code."
  (:require [clojure.data.priority-map :refer [priority-map]]))

(defn bfs
  "Breadth-first search from a start node.

   Parameters:
   - start: Starting node
   - neighbors-fn: Function that takes a node and returns neighbors
   - goal?: Predicate function to test if a node is the goal (optional)

   Returns: Map with:
     - :visited - set of all visited nodes
     - :path - path to goal (if goal? provided and found)
     - :distances - map of node to distance from start
     - :parents - map of node to parent node"
  ([start neighbors-fn]
   (bfs start neighbors-fn nil))
  ([start neighbors-fn goal?]
   (loop [queue (conj clojure.lang.PersistentQueue/EMPTY start)
          visited #{start}
          distances {start 0}
          parents {start nil}]
     (if (empty? queue)
       {:visited visited
        :distances distances
        :parents parents}
       (let [current (peek queue)
             queue (pop queue)]
         (if (and goal? (goal? current))
           (let [path (loop [node current
                             path []]
                        (if (nil? node)
                          (reverse path)
                          (recur (parents node) (conj path node))))]
             {:visited visited
              :path path
              :distances distances
              :parents parents
              :goal current})
           (let [current-dist (distances current)
                 neighbors (filter #(not (visited %)) (neighbors-fn current))
                 new-distances (reduce (fn [acc neighbor]
                                         (assoc acc neighbor (inc current-dist)))
                                       distances
                                       neighbors)
                 new-parents (reduce (fn [acc neighbor]
                                       (assoc acc neighbor current))
                                     parents
                                     neighbors)
                 new-visited (into visited neighbors)
                 new-queue (reduce conj queue neighbors)]
             (recur new-queue new-visited new-distances new-parents))))))))

(defn bfs-all-paths
  "Find all nodes reachable from start using BFS.

   Parameters:
   - start: Starting node
   - neighbors-fn: Function that takes a node and returns neighbors

   Returns: Set of all reachable nodes"
  [start neighbors-fn]
  (:visited (bfs start neighbors-fn)))

(defn bfs-shortest-path
  "Find shortest path from start to goal using BFS.

   Parameters:
   - start: Starting node
   - neighbors-fn: Function that takes a node and returns neighbors
   - goal?: Predicate function to test if a node is the goal

   Returns: Vector representing the path, or nil if no path exists"
  [start neighbors-fn goal?]
  (:path (bfs start neighbors-fn goal?)))

(defn dijkstra
  "Dijkstra's algorithm for shortest path with weighted edges.

   Parameters:
   - start: Starting node
   - neighbors-fn: Function that takes a node and returns sequence of [neighbor cost] pairs
   - goal?: Predicate function to test if a node is the goal (optional)

   Returns: Map with:
     - :distances - map of node to minimum distance from start
     - :parents - map of node to parent node in shortest path
     - :path - path to goal (if goal? provided and found)
     - :goal - goal node (if found)"
  ([start neighbors-fn]
   (dijkstra start neighbors-fn nil))
  ([start neighbors-fn goal?]
   (loop [queue (priority-map start 0)
          distances {start 0}
          parents {start nil}
          visited #{}]
     (if (empty? queue)
       {:distances distances
        :parents parents}
       (let [[current current-dist] (peek queue)
             queue (pop queue)]
         (if (visited current)
           (recur queue distances parents visited)
           (if (and goal? (goal? current))
             (let [path (loop [node current
                               path []]
                          (if (nil? node)
                            (reverse path)
                            (recur (parents node) (conj path node))))]
               {:distances distances
                :parents parents
                :path path
                :goal current
                :distance current-dist})
             (let [neighbors (neighbors-fn current)
                   updates (for [[neighbor cost] neighbors
                                 :let [new-dist (+ current-dist cost)
                                       old-dist (get distances neighbor Double/POSITIVE_INFINITY)]
                                 :when (< new-dist old-dist)]
                             [neighbor new-dist])
                   new-distances (reduce (fn [acc [neighbor dist]]
                                           (assoc acc neighbor dist))
                                         distances
                                         updates)
                   new-parents (reduce (fn [acc [neighbor _]]
                                         (assoc acc neighbor current))
                                       parents
                                       updates)
                   new-queue (reduce (fn [q [neighbor dist]]
                                       (assoc q neighbor dist))
                                     queue
                                     updates)]
               (recur new-queue new-distances new-parents (conj visited current))))))))))

(defn dijkstra-shortest-path
  "Find shortest path from start to goal using Dijkstra's algorithm.

   Parameters:
   - start: Starting node
   - neighbors-fn: Function that takes a node and returns sequence of [neighbor cost] pairs
   - goal?: Predicate function to test if a node is the goal

   Returns: Map with :path and :distance, or nil if no path exists"
  [start neighbors-fn goal?]
  (let [result (dijkstra start neighbors-fn goal?)]
    (when (:path result)
      {:path (:path result)
       :distance (:distance result)})))

(defn a-star
  "A* pathfinding algorithm.

   Parameters:
   - start: Starting node
   - neighbors-fn: Function that takes a node and returns sequence of [neighbor cost] pairs
   - heuristic-fn: Function that estimates distance from a node to the goal
   - goal?: Predicate function to test if a node is the goal

   Returns: Map with:
     - :path - path from start to goal
     - :distance - actual cost of the path
     - :goal - goal node"
  [start neighbors-fn heuristic-fn goal?]
  (loop [queue (priority-map start (heuristic-fn start))
         g-scores {start 0}
         parents {start nil}
         visited #{}]
    (if (empty? queue)
      nil
      (let [[current _] (peek queue)
            queue (pop queue)]
        (if (visited current)
          (recur queue g-scores parents visited)
          (if (goal? current)
            (let [path (loop [node current
                              path []]
                         (if (nil? node)
                           (reverse path)
                           (recur (parents node) (conj path node))))]
              {:path path
               :distance (g-scores current)
               :goal current})
            (let [current-g (g-scores current)
                  neighbors (neighbors-fn current)
                  updates (for [[neighbor cost] neighbors
                                :let [tentative-g (+ current-g cost)
                                      old-g (get g-scores neighbor Double/POSITIVE_INFINITY)]
                                :when (< tentative-g old-g)]
                            [neighbor tentative-g])
                  new-g-scores (reduce (fn [acc [neighbor g]]
                                         (assoc acc neighbor g))
                                       g-scores
                                       updates)
                  new-parents (reduce (fn [acc [neighbor _]]
                                        (assoc acc neighbor current))
                                      parents
                                      updates)
                  new-queue (reduce (fn [q [neighbor g]]
                                      (assoc q neighbor (+ g (heuristic-fn neighbor))))
                                    queue
                                    updates)]
              (recur new-queue new-g-scores new-parents (conj visited current)))))))))

(defn flood-fill
  "Flood fill from a starting position.

   Parameters:
   - start: Starting node
   - neighbors-fn: Function that takes a node and returns neighbors

   Returns: Set of all reachable nodes"
  [start neighbors-fn]
  (loop [queue (conj clojure.lang.PersistentQueue/EMPTY start)
         visited #{start}]
    (if (empty? queue)
      visited
      (let [current (peek queue)
            queue (pop queue)
            neighbors (filter #(not (visited %)) (neighbors-fn current))
            new-visited (into visited neighbors)
            new-queue (reduce conj queue neighbors)]
        (recur new-queue new-visited)))))

(defn count-paths
  "Count all paths from start to goal (use with caution - can be exponential!).

   Parameters:
   - start: Starting node
   - neighbors-fn: Function that takes a node and returns neighbors
   - goal?: Predicate function to test if a node is the goal

   Returns: Number of distinct paths"
  [start neighbors-fn goal?]
  (letfn [(count-from [current visited]
            (if (goal? current)
              1
              (let [neighbors (filter #(not (visited %)) (neighbors-fn current))]
                (reduce + 0 (map #(count-from % (conj visited current)) neighbors)))))]
    (count-from start #{})))
