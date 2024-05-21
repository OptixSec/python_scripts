from flask import Flask, request, jsonify

app = Flask(__name__)

# Store peers in a dictionary: {info_hash: {peer_id: (ip, port, last_announce_time)}}
peers = {}

# Store a list of known torrents
known_torrents = set()


@app.route("/announce", methods=["GET"])
def announce():
    info_hash = request.args.get("info_hash")
    peer_id = request.args.get("peer_id")
    ip = request.args.get("ip") or request.remote_addr
    port = int(request.args.get("port"))

    # If the torrent is not known, reject the announce
    if info_hash not in known_torrents:
        return jsonify({"error": "Unknown torrent"}), 400

    if info_hash not in peers:
        peers[info_hash] = {}

    peers[info_hash][peer_id] = (ip, port, time.time())

    # Remove stale peers (not announced for more than 30 minutes)
    timeout = 30 * 60
    current_time = time.time()
    peers[info_hash] = {
        pid: pdata
        for pid, pdata in peers[info_hash].items()
        if current_time - pdata[2] < timeout
    }

    # Respond with the list of peers
    response_peers = [
        {"ip": pdata[0], "port": pdata[1]} for pid, pdata in peers[info_hash].items()
    ]
    return jsonify({"peers": response_peers})


@app.route("/add_torrent", methods=["POST"])
def add_torrent():
    data = request.get_json()
    info_hash = data.get("info_hash")

    if not info_hash:
        return jsonify({"error": "info_hash is required"}), 400

    known_torrents.add(info_hash)
    return jsonify({"message": "Torrent added successfully"}), 200


@app.route("/list_torrents", methods=["GET"])
def list_torrents():
    return jsonify({"torrents": list(known_torrents)}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
