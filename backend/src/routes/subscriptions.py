from uuid import UUID

from fastapi import FastAPI, Response, APIRouter, HTTPException
from src.models.subscriptions import SubscribeRequest, SubscriptionReviewsResponse, SubscriptionReviewsRequest, \
    SubscriptionReviewsRequestByPublisher, SubscriptionsRequest
from src.database.db_instance import db_handler
from src.models.reviews import ReviewData
from src.models.user import UserData
import logging

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("", status_code=200)
async def subscribe(request: SubscribeRequest):
    if not request.publisher_id:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "message": "User id not found"
        })
    err = db_handler.addSubscription(subscribed_id=request.publisher_id, follower_id=request.subscriber_id)
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


@router.delete("", status_code=200)
async def unsubscribe(request: SubscribeRequest):
    if not request.publisher_id:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "message": "Subscription not found"
        })
    err = db_handler.deleteSubscription(follower_id=request.subscriber_id, subscribed_id=request.publisher_id)
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


@router.post("/publisher_reviews", status_code=200)
async def get_reviews(request: SubscriptionReviewsRequestByPublisher):
    if not request.publisher_id:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "message": "Publisher not found"
        })
    data, err = db_handler.getPublisherReviews(follower_id=request.subscriber_id, publisher_id=request.publisher_id)
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


@router.post("/all_reviews", status_code=200)
async def get_all_reviews(request: SubscriptionReviewsRequest):
    if not request.subscriber_id:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "message": "Subscriber ID is required"
        })

    data, err = db_handler.getAllReviews(follower_id=request.subscriber_id)

    if err:
        logging.info(f"Database returned error: {err}")
        if isinstance(err, ValueError):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "message": str(err)
            })
        else:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "message": "Unexpected database error"
            })

    answer = [
        ReviewData(
            rate=review.rate,
            text=review.text,
            book_id=review.book_id,
            user_id=review.user_id,
            created_at=review.created_at
        )
        for review in data
    ]

    return {
        "status": "success",
        "message": "Reviews retrieved successfully",
        "data": answer
    }

@router.post("/all_subscriptions", status_code=200)
async def get_all_subscriptions(request: SubscriptionsRequest):
    data, err = db_handler.getPublishers(follower_id=request.user_id)

    if err:
        logging.info(f"Database returned error: {err}")
        if isinstance(err, ValueError):
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "message": str(err)
            })
        else:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "message": "Unexpected database error"
            })

    answer = [
        UserData(
            name=user.name,
        )
        for user in data
    ]

    return {
        "status": "success",
        "message": "Subscriptions retrieved successfully",
        "data": answer
    }
