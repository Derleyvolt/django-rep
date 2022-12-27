var p = fetch('/foo')
  .then(res => res.status, err => console.error(err))