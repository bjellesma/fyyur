window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};
if(window.location.href.includes("venues/")){
  document.getElementById('deleteVenue').addEventListener('click', (event) => {
    const venueId = event.currentTarget.getAttribute('data-id')
    fetch(`/venues/${venueId}/delete`, {
      method: 'DELETE',
      body: JSON.stringify({
        'venueId': venueId
      }),
      headers: {
        'content-type': 'application/json'
      }
    }).then(
      response => window.location.replace('/')
    )
  })
}
if(window.location.href.includes('artists/')){
  document.getElementById('deleteArtist').addEventListener('click', (event) => {
    const artistId = event.currentTarget.getAttribute('data-id')
    fetch(`/artists/${artistId}/delete`, {
      method: 'DELETE',
      body: JSON.stringify({
        'artistId': artistId
      }),
      headers: {
        'content-type': 'application/json'
      }
    }).then(
      response => window.location.replace('/')
    )
  })
}

