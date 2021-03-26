import React, { useEffect, useRef } from "react";
import useResizeAware from "react-resize-aware";
import PropTypes from "prop-types";
import Neovis from "neovis.js/dist/neovis.js";

const NeoGraph = (props) => {
  const {
    width,
    height,
    containerId,
    backgroundColor,
    neo4jUri,
    neo4jUser,
    neo4jPassword,
  } = props;

  const visRef = useRef();

  useEffect(() => {
    const config = {
      container_id: visRef.current.id,
      server_url: neo4jUri,
      server_user: neo4jUser,
      server_password: neo4jPassword,
	  server_database: "youtube",
      initial_cypher:
        "MATCH (n)-[r:PRESENT|IS_PART_OF|AT|DURING]->(m) RETURN n,r,m LIMIT 100 ",
    };
    const vis = new Neovis(config);
    vis.render();
  }, [neo4jUri, neo4jUser, neo4jPassword]);

  return (
    <div
      id={containerId}
      ref={visRef}
      style={{
        width: "100%",
        height: "100%",
      }}
    />
  );
};

NeoGraph.defaultProps = {
	width: 600,
	height: 600,
	backgroundColor: "#d3d3d3",
  };
  
  NeoGraph.propTypes = {
	containerId: PropTypes.string.isRequired,
	neo4jUri: PropTypes.string.isRequired,
	neo4jUser: PropTypes.string.isRequired,
	neo4jPassword: PropTypes.string.isRequired,
  };

const ResponsiveNeoGraph = (props) => {
  const neoGraphProps = { ...props};
  return (
    <div style={{ position: "relative" }}>
      <NeoGraph {...neoGraphProps} />
    </div>
  );
};

ResponsiveNeoGraph.propTypes = {
  containerId: PropTypes.string.isRequired,
  neo4jUri: PropTypes.string.isRequired,
  neo4jUser: PropTypes.string.isRequired,
  neo4jPassword: PropTypes.string.isRequired,
};

export {NeoGraph,ResponsiveNeoGraph };