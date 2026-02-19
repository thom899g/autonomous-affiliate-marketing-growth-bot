from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CampaignPerformance(Base):
    __tablename__ = "campaign_performance"
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(String(50))
    date = Column(String(10))
    impressions = Column(Integer)
    clicks = Column(Integer)
    spend = Column(Float)
    revenue = Column(Float)

class DataManager:
    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri)
        
    def store_performance(self, campaign_id: str, date: str, 
                        impressions: int, clicks: int, spend: float, revenue: float) -> None:
        """
        Stores daily performance metrics.
        Args:
            campaign_id: ID of the campaign.
            date: Date in 'YYYY-MM-DD' format.
            impressions: Number of impressions.
            clicks: Number of clicks.
            spend: Advertising spend.
            revenue: Revenue generated.
        """
        try:
            with session_scope(self.engine) as session:
                performance = CampaignPerformance(
                    campaign_id=campaign_id,
                    date=date,
                    impressions=impressions,
                    clicks=clicks,
                    spend=spend,
                    revenue=revenue
                )
                session.add(performance)
                session.commit()
        except Exception as e:
            logging.error(f"Failed to store performance data: {str(e)}")
            raise

    def get_performance_report(self, campaign_id: str, start_date: str, end_date: str) -> List[Dict]:
        """
        Retrieves performance report for a campaign.
        Args:
            campaign_id: ID of the campaign.
            start_date: Start date in 'YYYY-MM-DD' format.
            end_date: End date in 'YYYY-MM-DD' format.
        Returns:
            List of performance metrics.
        """
        try:
            with session_scope(self.engine) as session:
                query = session.query(CampaignPerformance).filter(
                    CampaignPerformance.campaign_id == campaign_id,
                    CampaignPerformance.date >= start_date,
                    CampaignPerformance.date <= end_date
                )
                
                result = []
                for row in query.all():
                    result.append({
                        'date': row.date,
                        'impressions': row.impressions,
                        'clicks': row.clicks,
                        'spend': row.spend,
                        'revenue': row.revenue
                    })
                    
                return result
        except Exception as e:
            logging.error(f"Failed to retrieve performance report: {str(e)}")
            raise

def session_scope(engine):
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()