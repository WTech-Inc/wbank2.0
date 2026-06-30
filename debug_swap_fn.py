"""Debug swap page rendering"""
import sys, os
sys.stdout.reconfigure(encoding="utf-8")
os.environ["dataurl"] = "postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

sys.path.insert(0, "E:/wbank")
from main import app
from models import cashout, swap_config, audit_log
from extensions import db

with app.app_context():
    swaps = cashout.query.order_by(cashout.id.desc()).all()
    print(f"Swaps: {len(swaps)}")
    for s in swaps:
        audit = audit_log.query.filter_by(username=s.name, action="SWAP_APPLY").order_by(audit_log.timestamp.desc()).first()
        detail = audit.detail if audit else ""
        st = s.status or "Pending"
        print(f"  ID:{s.id} User:{s.name} HKD:{s.amount} Status:{st} Detail:{detail[:50]}")
        print(f"  Has Approve button: {st == 'Pending'}")
