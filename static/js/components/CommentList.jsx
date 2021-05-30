import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { useSelector, useDispatch } from "react-redux";
import { Button } from "@material-ui/core";
import Tooltip from "@material-ui/core/Tooltip";
import GroupIcon from "@material-ui/icons/Group";
import PropTypes from "prop-types";

import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import relativeTime from "dayjs/plugin/relativeTime";
import emoji from "emoji-dictionary";

import * as sourceActions from "../ducks/source";
import styles from "./CommentList.css";
import CommentEntry from "./CommentEntry";
import UserAvatar from "./UserAvatar";
import CommentAttachmentPreview from "./CommentAttachmentPreview";

dayjs.extend(relativeTime);
dayjs.extend(utc);

const CommentList = ({
  associatedResourceType = "object",
  objID = null,
  spectrumID = null,
}) => {
  const [hoverID, setHoverID] = useState(null);

  const handleMouseHover = (id, userProfile, author) => {
    if (
      userProfile.permissions.includes("System admin") ||
      userProfile.username === author
    ) {
      setHoverID(id);
    }
  };

  const handleMouseLeave = () => {
    setHoverID(null);
  };

  const dispatch = useDispatch();
  const obj = useSelector((state) => state.source);
  const spectra = useSelector((state) => state.spectra);
  const userProfile = useSelector((state) => state.profile);
  const permissions = useSelector((state) => state.profile.permissions);

  if (!objID) {
    objID = obj.id;
  }

  const addComment = (formData) => {
    dispatch(
      sourceActions.addComment({
        obj_id: objID,
        spectrum_id: spectrumID,
        ...formData,
      })
    );
  };
  const deleteComment = (id) => {
    dispatch(sourceActions.deleteComment(id, associatedResourceType));
  };

  let comments = null;
  if (associatedResourceType === "object") {
    comments = obj.comments;
  } else if (associatedResourceType === "spectrum") {
    if (spectrumID === null) {
      throw new Error("Must specify a spectrumID for comments on spectra");
    }
    const spectrum = spectra[objID].find((spec) => spec.id === spectrumID);
    comments = spectrum?.comments;
  } else {
    throw new Error(`Illegal input ${associatedResourceType} to CommentList. `);
  }

  // Color styling
  const userColorTheme = useSelector(
    (state) => state.profile.preferences.theme
  );
  const commentStyle =
    userColorTheme === "dark" ? styles.commentDark : styles.comment;

  comments = comments || [];

  const emojiSupport = (text) =>
    text.value.replace(/:\w+:/gi, (name) =>
      emoji.getUnicode(name) ? emoji.getUnicode(name) : name
    );

  return (
    <div className={styles.comments}>
      <div className={styles.commentsList}>
        {comments.map(
          ({ id, author, created_at, text, attachment_name, groups }) => (
            <span
              key={id}
              className={commentStyle}
              onMouseOver={() =>
                handleMouseHover(id, userProfile, author.username)
              }
              onMouseOut={() => handleMouseLeave()}
              onFocus={() => handleMouseHover(id, userProfile, author.username)}
              onBlur={() => handleMouseLeave()}
            >
              <div className={styles.commentUserAvatar}>
                <UserAvatar
                  size={24}
                  firstName={author.first_name}
                  lastName={author.last_name}
                  username={author.username}
                  gravatarUrl={author.gravatar_url}
                />
              </div>
              <div className={styles.commentContent}>
                <div className={styles.commentHeader}>
                  <span className={styles.commentUser}>
                    <span className={styles.commentUserName}>
                      {author.username}
                    </span>
                  </span>
                  <span className={styles.commentTime}>
                    {dayjs().to(dayjs.utc(`${created_at}Z`))}
                  </span>
                  <div className={styles.commentUserGroup}>
                    <Tooltip
                      title={groups.map((group) => group.name).join(", ")}
                    >
                      <GroupIcon fontSize="small" viewBox="0 -2 24 24" />
                    </Tooltip>
                  </div>
                </div>
                <div className={styles.wrap} name={`commentDiv${id}`}>
                  <ReactMarkdown
                    source={text}
                    escapeHtml={false}
                    className={styles.commentMessage}
                    renderers={{ text: emojiSupport }}
                  />
                  <Button
                    style={
                      hoverID === id
                        ? { display: "block" }
                        : { display: "none" }
                    }
                    size="small"
                    variant="outlined"
                    color="primary"
                    type="button"
                    name={`deleteCommentButton${id}`}
                    onClick={() => {
                      deleteComment(id);
                    }}
                    className={styles.commentDelete}
                  >
                    🗑
                  </Button>
                </div>
                <span>
                  {attachment_name && (
                    <CommentAttachmentPreview
                      filename={attachment_name}
                      commentId={id}
                    />
                  )}
                </span>
              </div>
            </span>
          )
        )}
      </div>
      <br />
      {permissions.indexOf("Comment") >= 0 && (
        <CommentEntry addComment={addComment} />
      )}
    </div>
  );
};

CommentList.propTypes = {
  objID: PropTypes.string,
  associatedResourceType: PropTypes.string,
  spectrumID: PropTypes.number,
};

CommentList.defaultProps = {
  objID: "",
  associatedResourceType: "object",
  spectrumID: null,
};

export default CommentList;
