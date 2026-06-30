"""
WCoins Blockchain — SHA-256 linked chain with CSV persistence
Total supply: 10,000,000 WCoins
"""
import hashlib
import datetime
import pytz
import os

WCOINS_TOTAL_SUPPLY = 10_000_000
CSV_PATH = "E:/wbank/wcoins_chain.csv"

class Block:
    def __init__(self, block_index, sender, receiver, amount, prev_hash="GENESIS"):
        self.block_index = block_index
        self.sender = sender
        self.receiver = receiver
        self.amount = str(amount)
        self.prev_hash = prev_hash
        self.status = "SUCCESS"
        self.created_at = datetime.datetime.utcnow()
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        ts = self.created_at.strftime("%Y-%m-%d %H:%M:%S.%f")
        data = f"{self.sender}->{self.receiver}->{self.amount}::{ts}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self):
        return {
            "block_index": self.block_index,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "hash": self.hash,
            "prev_hash": self.prev_hash,
            "status": self.status,
            "created_at": pytz.UTC.localize(self.created_at).astimezone(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S")
        }

class Blockchain:
    def __init__(self, db_session=None):
        self.db = db_session
    
    def _save_to_csv(self, block):
        """Append block to CSV file"""
        try:
            is_new = not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0
            with open(CSV_PATH, "a", encoding="utf-8") as f:
                if is_new:
                    f.write("block_index,sender,receiver,amount,hash,prev_hash,status,created_at\n")
                prev = block.prev_hash
                f.write(f"{block.block_index},{block.sender},{block.receiver},{block.amount},{block.hash},{prev},{block.status},{block.created_at}\n")
        except Exception as e:
            print(f"[CSV] Save error: {e}")
    
    def get_total_minted(self):
        """Get total WCoins minted so far"""
        if self.db:
            from sqlalchemy import text as sa_text
            total = self.db.execute(sa_text("SELECT COALESCE(SUM(CAST(amount AS DECIMAL)), 0) FROM wcoins_block WHERE sender != 'GENESIS'")).scalar()
            genesis = self.db.execute(sa_text("SELECT COALESCE(SUM(CAST(amount AS DECIMAL)), 0) FROM wcoins_block WHERE sender = 'GENESIS'")).scalar()
            return float(total) + float(genesis)
        return 0
    
    def _auto_repair(self):
        """Auto-fix chain hashes and prev_hash consistency"""
        import hashlib
        from sqlalchemy import text as st
        rows = self.db.execute(st("SELECT block_index, sender, receiver, amount, hash, prev_hash, created_at FROM wcoins_block ORDER BY block_index ASC")).fetchall()
        prev = "GENESIS"
        for r in rows:
            ts = r[6].strftime("%Y-%m-%d %H:%M:%S.%f")
            data = f"{r[1]}->{r[2]}->{r[3]}::{ts}"
            ch = hashlib.sha256(data.encode()).hexdigest()
            if ch != r[4]:
                self.db.execute(st("UPDATE wcoins_block SET hash=:h WHERE block_index=:i"), {"h": ch, "i": r[0]})
            if r[5] != prev:
                self.db.execute(st("UPDATE wcoins_block SET prev_hash=:p WHERE block_index=:i"), {"p": prev, "i": r[0]})
            prev = ch
        self.db.commit()

    def add_block(self, sender, receiver, amount):
        """Add a new block to the chain with supply check"""
        if self.db:
            from sqlalchemy import text as sa_text
            
            # Check supply cap
            current_total = self.get_total_minted()
            if current_total + float(amount) > WCOINS_TOTAL_SUPPLY:
                return None, f"Total supply exceeded! Max {WCOINS_TOTAL_SUPPLY}, current {current_total:.0f}"
            
            last = self.db.execute(
                sa_text("SELECT block_index, hash FROM wcoins_block ORDER BY block_index DESC LIMIT 1")
            ).fetchone()
            
            prev_hash = last[1] if last else "GENESIS"
            new_index = (last[0] + 1) if last else 1
            
            block = Block(new_index, sender, receiver, amount, prev_hash)
            
            self.db.execute(
                sa_text("INSERT INTO wcoins_block (block_index, sender, receiver, amount, hash, prev_hash, status, created_at) VALUES (:i, :s, :r, :a, :h, :p, :st, :c)"),
                {"i": block.block_index, "s": block.sender, "r": block.receiver, "a": block.amount, "h": block.hash, "p": block.prev_hash, "st": block.status, "c": block.created_at}
            )
            self.db.commit()
            
            # Save to CSV
            self._save_to_csv(block)
            
            return block, None
        return None, "DB not available"
    
    def get_chain(self, limit=50):
        """Get the full chain"""
        if self.db:
            from sqlalchemy import text as sa_text
            rows = self.db.execute(
                sa_text("SELECT block_index, sender, receiver, amount, hash, prev_hash, status, created_at FROM wcoins_block ORDER BY block_index DESC LIMIT :lim"),
                {"lim": limit}
            ).fetchall()
            return [{
                "block_index": r[0], "sender": r[1], "receiver": r[2],
                "amount": r[3], "hash": r[4], "prev_hash": r[5],
                "status": r[6], "created_at": pytz.UTC.localize(r[7]).astimezone(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S") if r[7] else ""
            } for r in rows]
        return []
    
    def get_user_tx(self, username, limit=20):
        """Get transactions for a user"""
        if self.db:
            from sqlalchemy import text as sa_text
            rows = self.db.execute(
                sa_text("SELECT block_index, sender, receiver, amount, hash, status, created_at FROM wcoins_block WHERE (sender=:u OR receiver=:u) AND sender != 'GENESIS' ORDER BY block_index DESC LIMIT :lim"),
                {"u": username, "lim": limit}
            ).fetchall()
            return [{
                "block_index": r[0], "sender": r[1], "receiver": r[2],
                "amount": r[3], "hash": r[4],
                "type": "sent" if r[1] == username else "received",
                "status": r[5], "created_at": pytz.UTC.localize(r[6]).astimezone(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S") if r[6] else ""
            } for r in rows]
        return []
    
    def repair_if_needed(self):
        """Repair chain if invalid, then return status"""
        result = self.verify_chain()
        if not result.get("valid"):
            self._auto_repair()
            result = self.verify_chain()
        return result

    def verify_chain(self):
        """Verify the entire chain"""
        if self.db:
            from sqlalchemy import text as sa_text
            rows = self.db.execute(
                sa_text("SELECT block_index, sender, receiver, amount, hash, prev_hash, created_at FROM wcoins_block ORDER BY block_index ASC")
            ).fetchall()
            
            results = []
            prev_hash = None
            for r in rows:
                ts = r[6].strftime("%Y-%m-%d %H:%M:%S.%f")
                data = f"{r[1]}->{r[2]}->{r[3]}::{ts}"
                calc_hash = hashlib.sha256(data.encode()).hexdigest()
                hash_ok = calc_hash == r[4]
                
                if prev_hash is None:
                    prev_ok = r[5] == "GENESIS"
                else:
                    prev_ok = r[5] == prev_hash
                
                results.append({
                    "block_index": r[0], "hash_ok": hash_ok, "prev_hash_ok": prev_ok,
                    "calculated_hash": calc_hash, "stored_hash": r[4],
                    "expected_prev": "GENESIS" if prev_hash is None else prev_hash, "stored_prev": r[5]
                })
                prev_hash = r[4]
            
            return {
                "total_blocks": len(rows),
                "valid": all(r["hash_ok"] and r["prev_hash_ok"] for r in results),
                "details": results
            }
        return {"total_blocks": 0, "valid": False, "details": []}
    
    def get_stats(self):
        if self.db:
            from sqlalchemy import text as sa_text
            count = self.db.execute(sa_text("SELECT COUNT(*) FROM wcoins_block")).scalar()
            total = self.db.execute(sa_text("SELECT COALESCE(SUM(CAST(amount AS DECIMAL)), 0) FROM wcoins_block")).scalar()
            genesis = self.db.execute(sa_text("SELECT CAST(amount AS DECIMAL) FROM wcoins_block WHERE sender='GENESIS' LIMIT 1")).scalar() or 0
            return {
                "blocks": count,
                "total_amount": float(total),
                "circulating": float(total) - float(genesis),
                "genesis_amount": float(genesis),
                "max_supply": WCOINS_TOTAL_SUPPLY,
                "remaining": WCOINS_TOTAL_SUPPLY - float(total)
            }
        return {"blocks": 0, "total_amount": 0}
'# TZ_TEST_MARKER'  
