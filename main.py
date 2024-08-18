import pubchempy as pcp
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def tanimoto(compound1, compound2):
    try:
        fp1 = int(compound1.fingerprint, 16)
        fp2 = int(compound2.fingerprint, 16)
        fp1_count = bin(fp1).count('1')
        fp2_count = bin(fp2).count('1')
        both_count = bin(fp1 & fp2).count('1')
        return float(both_count) / (fp1_count + fp2_count - both_count)
    except AttributeError:
        return 0.0


def search_pubchem_by_substring(substring):
    compounds = pcp.get_compounds(substring, 'name')
    filtered_compounds = []
    substring_lower = substring.lower()

    for compound in compounds:
        synonyms = [syn.lower() for syn in compound.synonyms if substring_lower in syn.lower()]
        if synonyms:
            filtered_compounds.append({
                'name': compound.iupac_name,
                'synonyms': synonyms[:5]
            })
        else:
            filtered_compounds.append({
                'name': compound.iupac_name,
                'synonyms': []
            })
    return filtered_compounds


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('query').lower()
    compounds = search_pubchem_by_substring(query)
    return jsonify(compounds)


def get_compound_data(compound_name):
    compound_info = pcp.get_compounds(compound_name, 'name')
    print(f"Search results for '{compound_name}': {compound_info}")
    if not compound_info or len(compound_info) == 0:
        return None
    compound = compound_info[0]
    fingerprint = getattr(compound, 'fingerprint', None)
    mol_data = compound.to_dict(properties=["atoms", "bonds"]) if compound.to_dict() else None
    compound_data = {
        'name': compound_name,
        'cid': compound.cid,
        'molecular_formula': compound.molecular_formula,
        'molecular_weight': compound.molecular_weight,
        'iupac_name': compound.iupac_name,
        'image_url': f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{compound.cid}/PNG",
        'mol_data': mol_data,
        'fingerprint': fingerprint
    }
    print(f"Compound data: {compound_data}")
    return compound_data


@app.route('/compare', methods=['POST'])
def compare():
    compound1_name = request.form.get('compound1')
    compound2_name = request.form.get('compound2')
    try:
        print(f"Received compounds: {compound1_name}, {compound2_name}")

        compound1_data = get_compound_data(compound1_name) if compound1_name else None
        compound2_data = get_compound_data(compound2_name) if compound2_name else None

        if compound1_name and not compound1_data:
            return jsonify({'error': f"The first compound '{compound1_name}' could not be found."})
        if compound2_name and not compound2_data:
            return jsonify({'error': f"The second compound '{compound2_name}' could not be found."})

        if compound1_data and compound2_data:
            if not compound1_data['fingerprint'] or not compound2_data['fingerprint']:
                return jsonify(
                    {'error': 'Unable to calculate similarity: one or both compounds do not have a fingerprint.'})

            similarity = tanimoto(pcp.Compound.from_cid(compound1_data['cid']),
                                  pcp.Compound.from_cid(compound2_data['cid']))

            comparison_data = {
                'compound1': compound1_data,
                'compound2': compound2_data,
                'similarity': round(similarity, 2)
            }

            print(f"Comparison data: {comparison_data}")
            return jsonify(comparison_data)
        elif compound1_data:
            return jsonify({'compound1': compound1_data})
        elif compound2_data:
            return jsonify({'compound2': compound2_data})
        else:
            return jsonify({'error': 'No valid compounds provided.'})

    except Exception as e:
        print(f"Comparison Error: {e}")
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
