from fastapi import FastAPI, Response, APIRouter, HTTPException
from src.models.subscriptions import SubscribeRequest, SubscriptionReviewsResponse, SubscriptionReviewsRequest
from src.database.db_instance import db_handler
from src.models.reviews import ReviewData
import logging

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("", status_code=200)
async def subscribe(request: SubscribeRequest):
    if not request.publisher_id:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "message": "User id not found"
        })
    err = db_handler.add_subscription(publisher_id=request.publisher_id, subscriber_id=request.subscriber_id)
    if err:
        logging.info(f"Database returned error: {err}")
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    logging.info("Function subscribe succeeded")
    return {
        "status": "success",
        "message": "Subscribed successfully"
    }


@router.delete("/{subscription_id}", status_code=200)
async def unsubscribe(subscription_id: int):
    if not subscription_id:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "message": "Subscription not found"
        })
    err = db_handler.delete_subscription(id=subscription_id)
    if err:
        logging.info(f"Database returned error: {err}")
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    logging.info("Function unsubscribe succeeded")
    return {
        "status": "success",
        "message": "Unsubscribed successfully"
    }


@router.get("/{subscription_id}/reviews", status_code=200)
async def get_reviews(subscription_id: int):
    if not subscription_id:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "message": "Subscription not found"
        })
    data, err = db_handler.get_reviews_from_subscription(id=subscription_id)
    answer = []
    if err:
        logging.info(f"Database returned error: {err}")
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    if data:
        for review in data:
            answer.append(ReviewData(
                rate=review.rate,
                text=review.text,
                book_id=review.book_id,
                user_id=review.user_id,
                created_at=review.created_at
            ))
    return {
        "status": "success",
        "message": "Reviews retrieved successfully",
        "data": answer
    }


@router.get("/all_reviews", status_code=200)
async def get_all_reviews(request: SubscriptionReviewsRequest):
    data, err = db_handler.get_reviews_using_subscriber(user_id=request.subscriber_id)
    answer = []
    if err:
        logging.info(f"Database returned error: {err}")
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": str(err)
        })
    if data:
        for review in data:
            answer.append(ReviewData(
                rate=review.rate,
                text=review.text,
                book_id=review.book_id,
                user_id=review.user_id,
                created_at=review.created_at
            ))
    return {
        "status": "success",
        "message": "Reviews retrieved",
        "data": answer
    }
